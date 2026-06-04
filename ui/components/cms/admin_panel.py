from probo import DIV, NAV, A, BUTTON, I, UL, LI, H4, P, FOOTER, SPAN
from django.urls import reverse
def admin_panel(is_collapsed=False):
    # Dynamic styling for the sidebar width
    sidebar_style = "width: 80px;" if is_collapsed else "width: 260px;"
    # Hide text labels if collapsed
    text_display = "d-none" if is_collapsed else "ms-2"

    sidebar = DIV(
            # Sidebar Header/Brand
            DIV(
                A(
                    I(Class="fas fa-shield-alt"), 
                    SPAN("Admin", Class=text_display)
                , href="/cms/admin/dashboard/", Class="navbar-brand text-white text-center w-100 mb-4"),
                A(
                    I(Class="fas fa-shield-alt"), 
                    SPAN("Store", Class=text_display)
                , href=reverse("cms:home"), Class="navbar-brand text-white text-center w-100 mb-4"),
            Class="p-3"),

            # Navigation Links
            UL(
                LI(A(I(Class="fas fa-home"), SPAN("Dashboard", Class=text_display), 
                     href="/cms/admin/dashboard/", Class="nav-link text-white p-3"), Class="nav-item"),
                LI(A(I(Class="fas fa-box"), SPAN("Products", Class=text_display), 
                     href="/cms/admin/products/dashboard/", Class="nav-link text-white p-3"), Class="nav-item"),
                LI(A(I(Class="fas fa-users"), SPAN("Clients", Class=text_display), 
                     href="/cms/admin/clients/dashboard/", Class="nav-link text-white p-3"), Class="nav-item"),
                LI(A(I(Class="fas fa-cog"), SPAN("Orders", Class=text_display), 
                     href="/cms/admin/orders/dashboard/", Class="nav-link text-white p-3"), Class="nav-item"),
                # LI(A(I(Class="fas fa-cog"), SPAN("Payments", Class=text_display), 
                    #  href="/cms/admin/payments/dashboard/", Class="nav-link text-white p-3"), Class="nav-item"),
                LI(A(I(Class="fas fa-cog"), SPAN("Content", Class=text_display), 
                     href="/cms/admin/content/dashboard/", Class="nav-link text-white p-3"), Class="nav-item"),
                # LI(A(I(Class="fas fa-cog"), SPAN("Wishlists", Class=text_display), 
                #      href="/cms/admin/wishlists/dashboard/", Class="nav-link text-white p-3"), Class="nav-item"),
            Class="nav flex-column"),
                BUTTON(
                I(Class=f"fas {'fa-chevron-right' if is_collapsed else 'fa-chevron-left'}"),
                Class="btn btn-link text-white mt-auto p-3 text-center",
                hx_get=f"cms/admin/toggle-sidebar?collapsed={'false' if is_collapsed else 'true'}",
                hx_target="#admin-wrapper",
                hx_swap="outerHTML"
            ),
        id="sidebar",
        Class="bg-dark d-flex flex-column vh-100 transition-all sticky-top",
        style=sidebar_style
    )

    main_content = DIV(
        # Top Bar (Where the original nav content might go)
        NAV(
            H4("Manage Inventory", Class="mb-0 fs-5"),
            Class="navbar navbar-light bg-white border-bottom p-3 shadow-sm",
        ),
        # Page Body
        DIV(
            Class="p-4 flex-grow-1",
            data_ssdom_id="root-container",
        ),
        # Footer
        FOOTER(
            P("© 2026 E-commerce Admin", Class="text-muted mb-0 small"),
            Class="bg-white border-top p-3 text-center",
        ),
        Class="flex-grow-1 d-flex flex-column",
        style="overflow-y: auto;",
    )

    return DIV(
        sidebar,
        main_content,
        id="admin-wrapper",
        Class="d-flex w-100 vh-100",
    )
