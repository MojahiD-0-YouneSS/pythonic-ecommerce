from probo import DIV, H3, H4, H5, H6, P, SPAN, I, A, BUTTON, IMG, SMALL, SECTION
from apps.global_context import get_global_context

def ContentRow(item, icon_class):
    """A generic row for listing any CMS content."""
    is_active = item.get('status') == 'Active'
    status_color = "success" if is_active else "secondary"
    
    # Extract extra info based on content type (author for quotes, placement for posters, etc.)
    extra_info = item.get('type') or item.get('author') or item.get('placement') or ""

    return DIV(
        # Icon & Title
        DIV(
            DIV(
                I(Class=f"bi {icon_class} fs-5 text-primary"),
                Class="bg-light rounded p-2 me-3 d-flex align-items-center justify-content-center",
                style="width: 45px; height: 45px;"
            ),
            DIV(
                H6(item.get('title'), Class="mb-0 fw-bold"),
                SMALL(extra_info, Class="text-muted"),
                Class="flex-grow-1"
            ),
            Class="col-5 d-flex align-items-center"
        ),
        
        # Status
        DIV(
            SPAN(item.get('status'), Class=f"badge bg-{status_color} smaller"),
            Class="col-2 text-center"
        ),
        
        # Date
        DIV(
            SMALL(item.get('updated'), Class="text-muted smaller"),
            Class="col-2 text-center"
        ),
        
        # Actions
        DIV(
            A(I(Class="bi bi-pencil"), href=f"/admin/content/edit/{item.get('id')}/", Class="btn btn-xs btn-outline-secondary me-2"),
            BUTTON(I(Class="bi bi-trash"), Class="btn btn-xs btn-outline-danger", hx_delete=f"/admin/content/delete/{item.get('id')}/", hx_confirm="Delete this content?"),
            Class="col-3 text-end"
        ),
        Class="row align-items-center py-3 border-bottom hover-bg-light g-0 px-3 last-border-0"
    )

def ContentSection(title, items, icon_class):
    """Wrapper for a specific content type list."""
    return SECTION(
        DIV(
            H6(title, Class="text-muted text-uppercase fw-bold mb-0 smaller"),
            A(I(Class="bi bi-plus-lg me-1"), "Add New", href="#", Class="btn btn-sm btn-primary"),
            Class="d-flex justify-content-between align-items-center mb-3"
        ),
        DIV(
            *[ContentRow(item, icon_class) for item in items] if items else [P("No content found.", Class="p-3 text-muted small mb-0")],
            Class="bg-white border rounded shadow-sm overflow-hidden"
        ),
        Class="mb-5"
    )

# --- 3. ORCHESTRATOR ---

def SiteContentDashboard():
    """
    Main Orchestrator for the Content Management Hub.
    """
    mock_content_context = {
    "banners": [
        {"id": 1, "title": "Summer Sale Hero", "status": "Active", "type": "Hero", "updated": "2 days ago"},
        {"id": 2, "title": "Winter Clearance", "status": "Draft", "type": "Hero", "updated": "1 month ago"},
    ],
    "quotes": [
        {"id": 1, "title": "CEO Welcome", "author": "John Doe", "status": "Active", "updated": "1 week ago"},
        {"id": 2, "title": "Customer Testimonial 1", "author": "Sarah M.", "status": "Active", "updated": "3 days ago"},
    ],
    "posters": [
        {"id": 1, "title": "Free Shipping Promo", "placement": "Sidebar", "status": "Active", "updated": "Yesterday"},
    ]
}

    context = get_global_context()
    banners = context.get('banners', mock_content_context['banners'])
    quotes = context.get('quotes', mock_content_context['quotes'])
    posters = context.get('posters', mock_content_context['posters'])

    return DIV(
        # Header
        DIV(
            H3("Site Content Management", Class="fw-bold mb-1"),
            P("Manage banners, promotional posters, and dynamic text quotes.", Class="text-muted"),
            Class="mb-5"
        ),

        # Content Sections
        DIV(
            DIV(ContentSection("Hero Banners", banners, "bi-images"), Class="col-lg-12"),
            DIV(ContentSection("Promotional Posters", posters, "bi-file-post"), Class="col-lg-6"),
            DIV(ContentSection("Quotes & Testimonials", quotes, "bi-chat-quote"), Class="col-lg-6"),
            Class="row"
        ),

        Class="container-fluid py-4",
        id="content-admin-hub"
    )
