from probo import DIV, FORM, INPUT, LABEL, H5, SPAN, I, BUTTON, SCRIPT
from django.urls import reverse

def CategoryFilterSidebar(categories, selected_category_ids=None):
    """
    Renders a premium, interactive Category filter panel.

    :param categories: List of dictionary/model instances (e.g., [{'id': 1, 'name': 'Category 1'}])
    :param selected_category_ids: List of currently checked category IDs (for persistence)
    """
    if selected_category_ids is None:
        selected_category_ids = []

    # Map selected IDs to strings for easy comparison
    selected_set = {str(cid) for cid in selected_category_ids}
    url = reverse("product:product-filter")
    # Generate the list of checkbox elements
    checkbox_elements = []
    for cat in categories:
        cat_id = str( cat.id if hasattr(cat,'id') else cat.get("id"))
        cat_name = str(cat.name if hasattr(cat, "name") else cat.get("name"))
        is_checked = cat_id in selected_set

        checkbox_elements.append(
            DIV(
                INPUT(
                    Type="checkbox",
                    name="category",
                    value=cat_id,
                    id=f"cat-check-{cat_id}",
                    Class="form-check-input border-secondary-subtle",
                    checked=is_checked,
                ),
                LABEL(
                    cat_name,
                    Class="form-check-label text-dark-emphasis fw-medium ps-2 cursor-pointer w-100",
                    For=f"cat-check-{cat_id}",
                ),
                # data-search attribute is what our inline JS will scan!
                Class="form-check d-flex align-items-center mb-2.5 py-1 rounded transition-all filter-item-row",
                style="transition: all 0.2s ease;",
                data_search=cat_name.lower(),
            )
        )

    return DIV(
        # Sidebar Header with an HTMX-powered Clear button
        DIV(
            H5("Categories", Class="fw-bold text-dark m-0 fs-5"),
            BUTTON(
                "Clear",
                Type="button",
                Class="btn btn-sm btn-link text-decoration-none text-muted p-0 fw-semibold",
                **(
                    {
                        "hx-get": f"{url}?clear=true",
                        "hx-target": "#product-grid-container",
                        "hx-swap": "outerHTML",
                    }
                    if selected_category_ids
                    else {"style": "display: none;"}
                ),
            ),
            Class="d-flex justify-content-between align-items-center mb-3",
        ),
        # Mini Search Bar (Instant client-side filter)
        DIV(
            INPUT(
                Type="text",
                id="category-search-input",
                placeholder="Search categories...",
                Class="form-control form-control-sm border-0 bg-light py-2 px-3 rounded-3 shadow-none mb-3",
                onkeyup="filterCategoryList(this.value)",  # Fires instant client-side filter
            ),
            Class="position-relative",
        ),
        # Interactive Form Wrapper
        FORM(
            # Scrollable Checkbox Container
            DIV(
                *checkbox_elements,
                id="category-checkbox-container",
                Class="pe-1",
                style="max-height: 350px; overflow-y: auto; scrollbar-width: thin;",
            ),
            # --- HTMX AUTO-SUBMIT MAGIC ---
            # Any change inside this form triggers a GET request with all selected categories serialized.
            hx_get=url,
            hx_target="#product-grid-container",
            hx_trigger="change delay:100ms",
            hx_swap="outerHTML",
        ),
        # Tiny client-side search script to keep interactions sub-millisecond
        SCRIPT("""
            function filterCategoryList(query) {
                const lowerQuery = query.toLowerCase().trim();
                const items = document.querySelectorAll('.filter-item-row');
                
                items.forEach(item => {
                    const text = item.getAttribute('data-search') || '';
                    if (text.includes(lowerQuery)) {
                        item.style.setProperty('display', 'flex', 'important');
                    } else {
                        item.style.setProperty('display', 'none', 'important');
                    }
                });
            }
        """),
        Class="col-3 card border-0 shadow-sm p-4 rounded-4 bg-white",
    )
