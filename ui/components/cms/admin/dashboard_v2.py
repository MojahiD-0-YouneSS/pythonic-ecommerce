from probo import DIV, H3, H4, H5, H6, P, SPAN, I, A, BUTTON, IMG, SMALL, SECTION, HR 
from django.urls import reverse
from django_abstract.utilities import to_snake_case
from ui.components.shared.form_modal import AdminEditModal

# --- 1. REUSABLE UI COMPONENTS ---


def MediaAdminCard() -> DIV:
    """
    A visual card for CMS models that contain Media (Images/Videos).
    Includes a thumbnail preview and a prominent toggle button.
    """

    # The toggle button flips between 'Hide' and 'Publish' states

    def resolve_image(**dvars) -> IMG|DIV:
        obj = dvars.get('obj')

        image_url =  obj.image.url if hasattr(obj, "image") else obj.customer_image.url if hasattr(obj, "customer_image") else None
        if image_url:
            return IMG(
                src=image_url,
                Class="card-img-top object-fit-cover",
                style="height: 140px;",
            )
        else:
            return DIV(
                I(Class="bi bi-image text-muted fs-1"),
                Class="bg-light d-flex justify-content-center align-items-center w-100",
                style="height: 140px;",
            )


    return DIV(
        # Top: Image Preview
        DIV(
            {'obj',resolve_image},
            SPAN(
                {'obj',lambda **dvars:"Active" if getattr(dvars.get('obj'),'is_active',False) else "Hidden"},
                Class={'obj', lambda **dvars: (
                    f'position-absolute top-0 end-0 badge bg-{"success" if getattr(dvars.get("obj"), "is_active", False) else "secondary"} m-2 shadow-sm')},
            ),
            Class="position-relative border-bottom",
        ),
        # Bottom: Metadata & Actions
        DIV(
            H6({'obj',lambda **dvars:dvars.get('obj').title if hasattr(dvars.get('obj'), "title") else dvars.get('obj').customer_name if hasattr(dvars.get('obj'), "customer_name") else dvars.get('obj').name if hasattr(dvars.get('obj'), "name") else "Untitled"}, Class="fw-bold mb-1 text-truncate"),
            SMALL({'obj',lambda **dvars:dvars.get('obj').subtitle if hasattr(dvars.get('obj'), "subtitle") else dvars.get('obj').description if hasattr(dvars.get('obj'), "description") else dvars.get('obj').content if hasattr(dvars.get('obj'), "content") else "No description"}, Class="text-muted d-block text-truncate mb-3"),
            # HTMX Action Buttons
            DIV(
                # Toggle Active Status
                BUTTON(
                    I(Class={"obj",lambda **dvars:f'bi {"bi-eye-slash-fill" if getattr(dvars.get("obj",),"is_active",False) else "bi-eye-fill"}'}),
                    {"obj",lambda **dvars:"Hide" if getattr(dvars.get("obj",),"is_active",False) else "Publish"},
                    Class={"obj", lambda **dvars:f'btn btn-sm w-100 mb-2 fw-bold {"btn-outline-warning" if getattr(dvars.get("obj",),"is_active",False) else "btn-outline-success"}'},
                    hx_post={'obj', lambda **dvars:reverse(
                        "cms:admin-hide-media", kwargs={"slug": f"select_{to_snake_case(dvars.get('obj').__class__.__name__)}", "id": getattr(dvars.get('obj'),'id',None)}
                    )},
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
                        hx_get={"obj",lambda **dvars:reverse(
                            "cms:admin-edit-media",
                            kwargs={"slug": f"select_{to_snake_case(dvars.get('obj').__class__.__name__)}",
                                    "id": getattr(dvars.get('obj'), 'id', None)}
                        )},
                        hx_target="#admin-edit-modal-body",  # Swaps just this card!
                        hx_swap="innerHTML",
                    ),
                    BUTTON(
                        I(Class="bi bi-trash"),
                        Class="btn btn-sm btn-outline-danger",
                        hx_delete={"obj",lambda **dvars:reverse(
                            "cms:admin-delete-media",
                            kwargs={"slug": f"select_{to_snake_case(dvars.get('obj').__class__.__name__)}",
                                    "id": getattr(dvars.get('obj'), 'id', None)}
                        )},
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


def TextAdminRow(title, subtitle, is_active, extra_info, icon_class, toggle_url, view_url, delete_url):
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
    if not items:
        return P("No media content found.", Class="text-muted p-3")
    for item in items:
        if item:
            cards.append(
            DIV(
                MediaAdminCard(),
                data_pipeline={'obj':item},
                Class="col-md-4 col-lg-3 mb-4",
            )
        )
    return DIV(*cards, Class="row")


def SiteContentDashboard():
    """
    Main Orchestrator for the Content Management Hub.
    Expects actual Django QuerySets passed in the context dictionary.
    """
    def process_banners(**dvars):
        banners= dvars.get("banners",) or  []
        if not banners:
            return P("No banners to show!.", Class="text-muted p-3")
        return render_media_grid(banners, "banner", "title", "subtitle", "image"),

    def process_posters(**dvars):
        posters= dvars.get("posters",) or  []
        if not posters:
            return P("No posters to show!.", Class="text-muted p-3")
        return render_media_grid(posters, "poster", "title", "description", "image")
    def process_system_banners(**dvars):
        system_banners= dvars.get("system_banners",) or  []
        if not system_banners:
            return P("No system_banners to show!.", Class="text-muted p-3")
        return render_media_grid(
            system_banners, "system-banner", "title", "link", "image"
        )
    def process_testimonies(**dvars):
        testimonies= dvars.get("testimonies",) or  []
        if not testimonies:
            return P("No testimonies to show!.", Class="text-muted p-3")
        return render_media_grid(
            testimonies, "testimony", "customer_name", "feedback", "customer_image"
        )
    def process_about_us(**dvars):
        about_us= dvars.get("about_us",) or  []
        if not about_us:
            return P("No about_us to show!.", Class="text-muted p-3")
        return render_media_grid(about_us, "about", "title", "content", "image")

    def process_quotes_and_contacts(**dvars):
        quotes= dvars.get("quotes",) or  []
        contacts= dvars.get("contacts",) or  []

        return DIV(
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
            ] if quotes else [P("No pending communications.", Class="text-muted p-3")],
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
            ] if contacts else [P("No pending communications.", Class="text-muted p-3")],
            Class="bg-white border rounded shadow-sm overflow-hidden")


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
                    href=reverse('cms:admin-banner-create'),
                    Class="btn btn-sm btn-dark",
                ),
                Class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2",
            ),
            H6(
                "Hero Banners",
                Class="text-muted small text-uppercase fw-bold mb-3 mt-4",
            ),
            {'banners',process_banners},
            DIV(
                H6(
                    "Promotional Posters",
                    Class="text-muted small text-uppercase fw-bold m-0",
                ),
                A(
                    I(Class="bi bi-plus-lg me-1"),
                    "Add Poster",
                    href=reverse("cms:admin-poster-create"),
                    Class="btn btn-sm btn-outline-dark",
                ),
                Class="d-flex justify-content-between align-items-center mb-3 mt-4",
            ),
            {'posters',process_posters},
            DIV(
                H6(
                    "System Wide Alerts",
                    Class="text-muted small text-uppercase fw-bold m-0",
                ),
                A(
                    I(Class="bi bi-plus-lg me-1"),
                    "Add System Banner",
                    href=reverse("cms:admin-systembanner-create"),
                    Class="btn btn-sm btn-outline-dark",
                ),
                Class="d-flex justify-content-between align-items-center mb-3 mt-4",
            ),
            {'system_banners',process_system_banners},
            Class="bg-light p-4 rounded-4 shadow-sm border mb-5",
        ),
        SECTION(
            DIV(
                H5("Brand & Social Proof", Class="fw-bold text-dark m-0"),
                Class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2",
            ),
            DIV(
                H6(
                    "About Us Sections",
                    Class="text-muted small text-uppercase fw-bold m-0",
                ),
                A(
                    I(Class="bi bi-plus-lg me-1"),
                    "Add About Us",
                    href=reverse("cms:admin-aboutus-create"),
                    Class="btn btn-sm btn-outline-dark",
                ),
                Class="d-flex justify-content-between align-items-center mb-3 mt-4",
            ),
            {'about_us',process_about_us},
            DIV(
                H6(
                    "Customer Testimonials",
                    Class="text-muted small text-uppercase fw-bold m-0",
                ),
                A(
                    I(Class="bi bi-plus-lg me-1"),
                    "Add Testimony",
                    href=reverse('cms:admin-testimony-create'),
                    Class="btn btn-sm btn-outline-dark",
                ),
                Class="d-flex justify-content-between align-items-center mb-3 mt-4",
            ),
            {'testimonies',process_testimonies},
            Class="bg-light p-4 rounded-4 shadow-sm border mb-5",
        ),
        # --- TEXT HEAVY SECTIONS ---
        SECTION(
            DIV(
                H5("Inbound Communications", Class="fw-bold text-dark m-0"),
                Class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2",
            ),
            {'quotes','contacts',process_quotes_and_contacts},
            AdminEditModal(),
        ),
        Class="container-fluid py-4",
        id="content-admin-hub",
    )
