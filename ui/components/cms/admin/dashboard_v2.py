from probo import DIV, H3, H4, H5, H6, P, SPAN, I, A, BUTTON, IMG, SMALL, SECTION, HR 
from django.urls import reverse
from django_abstract.utilities import to_snake_case
from ui.components.shared.form_modal import AdminEditModal
# --- 1. REUSABLE UI COMPONENTS ---


def MediaAdminCard(
    title, subtitle, image_url, is_active,**kwargs
):
    """
    A visual card for CMS models that contain Media (Images/Videos).
    Includes a thumbnail preview and a prominent toggle button.
    """
    status_color = "success" if is_active else "secondary"
    status_text = "Active" if is_active else "Hidden"
    obj_id = kwargs.get("obj_id", )
    slug = kwargs.get("slug", )
    # The toggle button flips between 'Hide' and 'Publish' states
    toggle_icon = "bi-eye-slash-fill" if is_active else "bi-eye-fill"
    toggle_text = " Hide" if is_active else " Publish"
    toggle_btn_class = "btn-outline-warning" if is_active else "btn-outline-success"

    return DIV(
        # Top: Image Preview
        DIV(
            (
                IMG(
                    src=image_url,
                    Class="card-img-top object-fit-cover",
                    style="height: 140px;",
                )
                if image_url
                else DIV(
                    I(Class="bi bi-image text-muted fs-1"),
                    Class="bg-light d-flex justify-content-center align-items-center w-100",
                    style="height: 140px;",
                )
            ),
            SPAN(
                status_text,
                Class=f"position-absolute top-0 end-0 badge bg-{status_color} m-2 shadow-sm",
            ),
            Class="position-relative border-bottom",
        ),
        # Bottom: Metadata & Actions
        DIV(
            H6(title, Class="fw-bold mb-1 text-truncate"),
            SMALL(subtitle, Class="text-muted d-block text-truncate mb-3"),
            # HTMX Action Buttons
            DIV(
                # Toggle Active Status
                BUTTON(
                    I(Class=f"bi {toggle_icon}"),
                    toggle_text,
                    Class=f"btn btn-sm w-100 mb-2 fw-bold {toggle_btn_class}",
                    hx_post=reverse(
                        "cms:admin-hide-media", kwargs={"slug": slug, "id": obj_id}
                    ),
                    hx_target="closest .card",  # Swaps just this card!
                    hx_swap="outerHTML",
                ),
                # Edit / Delete Row
                DIV(
                    BUTTON(
                        I(Class="bi bi-pencil"),
                        " Edit",
                        Class="btn btn-sm btn-light border flex-grow-1 me-2",
                        data_bs_toggle="modal",
                        data_bs_target="#adminEditModal",
                        hx_get=reverse(
                            "cms:admin-edit-media", kwargs={"slug": slug, "id": obj_id}
                        ),
                        hx_target="#admin-edit-modal-body",  # Swaps just this card!
                        hx_swap="innerHTML",
                    ),
                    BUTTON(
                        I(Class="bi bi-trash"),
                        Class="btn btn-sm btn-outline-danger",
                        hx_delete=reverse(
                            "cms:admin-delete-media", kwargs={"slug": slug, "id": obj_id}
                        ),
                        hx_target="closest .card",
                        hx_swap="outerHTML swap:0.5s",
                        hx_confirm="Delete this content forever?",
                    ),
                    Class="d-flex",
                ),
            ),
            Class="card-body p-3 bg-white",
        ),
        Class="card shadow-sm border-0 h-100 transition-all",
        style="min-width: 220px;",
    )


def TextAdminRow(
    title, subtitle, is_active, extra_info, icon_class, toggle_url, view_url, delete_url
):
    """
    A compact list row for text-heavy CMS models (Quotes, Contacts, etc.).
    """
    status_color = "success" if is_active else "secondary"
    status_text = "Active" if is_active else "Resolved/Hidden"

    return DIV(
        # Icon & Text
        DIV(
            DIV(
                I(Class=f"bi {icon_class} fs-5 text-primary"),
                Class="bg-light rounded p-2 me-3 d-flex align-items-center justify-content-center border",
                style="width: 45px; height: 45px;",
            ),
            DIV(
                H6(title, Class="mb-0 fw-bold"),
                SMALL(
                    subtitle,
                    Class="text-muted text-truncate d-inline-block",
                    style="max-width: 300px;",
                ),
                Class="flex-grow-1",
            ),
            Class="col-5 d-flex align-items-center",
        ),
        # Extra Info / Status
        DIV(
            SPAN(extra_info, Class="text-muted smaller fw-medium"),
            Class="col-3 text-center",
        ),
        DIV(
            SPAN(status_text, Class=f"badge bg-{status_color} smaller"),
            Class="col-1 text-center",
        ),
        # Actions
        DIV(
            BUTTON(
                "Toggle",
                Class="btn btn-xs btn-outline-secondary me-2",
                hx_post=toggle_url,
                hx_target="closest .row",
                hx_swap="outerHTML",
            ),
            A("View", href=view_url, Class="btn btn-xs btn-primary me-2"),
            BUTTON(
                I(Class="bi bi-trash"),
                Class="btn btn-xs btn-danger",
                hx_delete=delete_url,
                hx_target="closest .row",
                hx_swap="outerHTML",
            ),
            Class="col-3 text-end",
        ),
        Class="row align-items-center py-3 border-bottom hover-bg-light g-0 px-3 transition-all",
    )

    # --- 2. ORCHESTRATOR ---

# Format Media Cards dynamically
def render_media_grid(items, type_slug, title_field, sub_field, img_field):
    cards = []
    for item in items:
        img = getattr(item, img_field)
        img_url = img.url if img else None
        is_active = getattr(item, "is_active", getattr(item, "is_approved", False))

        cards.append(
            DIV(
                MediaAdminCard(
                    title=getattr(item, title_field),
                    subtitle=getattr(item, sub_field, "No description"),
                    image_url=img_url,
                    is_active=is_active,
                    obj_id=item.id,
                    slug=f"select_{to_snake_case(item.__class__.__name__)}",
                ),
                Class="col-md-4 col-lg-3 mb-4",
            )
        )
    return (
        DIV(*cards, Class="row")
        if cards
        else P("No media content found.", Class="text-muted p-3")
    )


def SiteContentDashboard(context):
    """
    Main Orchestrator for the Content Management Hub.
    Expects actual Django QuerySets passed in the context dictionary.
    """
    # Extract ORM Querysets
    banners = context.get("banners", [])
    posters = context.get("posters", [])
    system_banners = context.get("system_banners", [])
    testimonies = context.get("testimonies", [])
    about_us = context.get("about_us", [])
    quotes = context.get("quotes", [])
    contacts = context.get("contacts", [])

    return DIV(
        # Header
        DIV(
            H3("Site Content & Media", Class="fw-bold mb-1"),
            P(
                "Manage hero banners, system alerts, visual media, and text content.",
                Class="text-muted",
            ),
            Class="mb-5",
        ),
        # --- MEDIA HEAVY SECTIONS ---
        SECTION(
            DIV(
                H5("Storefront Banners & Posters", Class="fw-bold text-dark m-0"),
                A(
                    I(Class="bi bi-plus-lg me-1"),
                    "Add Banner",
                    href="/custom-admin/cms/banner/add/",
                    Class="btn btn-sm btn-dark",
                ),
                Class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2",
            ),
            H6(
                "Hero Banners",
                Class="text-muted small text-uppercase fw-bold mb-3 mt-4",
            ),
            render_media_grid(banners, "banner", "title", "subtitle", "image"),
            H6(
                "Promotional Posters",
                Class="text-muted small text-uppercase fw-bold mb-3 mt-4",
            ),
            render_media_grid(posters, "poster", "title", "description", "image"),
            H6(
                "System Wide Alerts",
                Class="text-muted small text-uppercase fw-bold mb-3 mt-4",
            ),
            render_media_grid(
                system_banners, "system-banner", "title", "link", "image"
            ),
            Class="bg-light p-4 rounded-4 shadow-sm border mb-5",
        ),
        SECTION(
            DIV(
                H5("Brand & Social Proof", Class="fw-bold text-dark m-0"),
                Class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2",
            ),
            H6(
                "About Us Sections",
                Class="text-muted small text-uppercase fw-bold mb-3 mt-4",
            ),
            render_media_grid(about_us, "about", "title", "content", "image"),
            H6(
                "Customer Testimonials",
                Class="text-muted small text-uppercase fw-bold mb-3 mt-4",
            ),
            render_media_grid(
                testimonies, "testimony", "customer_name", "feedback", "customer_image"
            ),
            Class="bg-light p-4 rounded-4 shadow-sm border mb-5",
        ),
        # --- TEXT HEAVY SECTIONS ---
        SECTION(
            DIV(
                H5("Inbound Communications", Class="fw-bold text-dark m-0"),
                Class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2",
            ),
            (
                DIV(
                    *[
                        TextAdminRow(
                            title=f"Quote Request: {q.reference_code}",
                            subtitle=f"Product: {q.product.name} | Qty: {q.quantity}",
                            is_active=(q.status == "pending"),
                            extra_info=f"Proposed: ${q.proposed_price}",
                            icon_class="bi-receipt",
                            toggle_url=f"#",
                            view_url=f"#",
                            delete_url=f"#",
                        )
                        for q in quotes
                    ],
                    *[
                        TextAdminRow(
                            title=f"Contact: {c.full_name}",
                            subtitle=c.message,
                            is_active=c.is_active,
                            extra_info=c.email,
                            icon_class="bi-envelope-paper",
                            toggle_url=f"#",
                            view_url=f"#",
                            delete_url=f"#",
                        )
                        for c in contacts
                    ],
                    Class="bg-white border rounded shadow-sm overflow-hidden",
                )
                if (quotes or contacts)
                else P("No pending communications.", Class="text-muted p-3")
            ),
            AdminEditModal(),
        ),
        Class="container-fluid py-4",
        id="content-admin-hub",
    )
