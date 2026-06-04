from probo import DIV, NAV, A, BUTTON, INPUT, SPAN, UL, LI, FOOTER, P, I 
from django.urls import reverse
from ui.components.cart.icon import cart_icon

def ClientHeader(cart_count=0,user_status=None,is_admin=False) -> NAV:

    return NAV(
        DIV(
            # Brand
            A("PY-STORE", href="/", Class="navbar-brand fw-bold fs-4"),
            # Mobile Toggle
            BUTTON(
                SPAN(Class="navbar-toggler-icon"),
                Class="navbar-toggler",
                Type="button",
                data_bs_toggle="collapse",
                data_bs_target="#navContent",
            ),
            DIV(
                # Search Bar
                DIV(
                    INPUT(
                        type="search",
                        placeholder="Search products...",
                        Class="form-control rounded-pill",
                    ),
                    Class="mx-auto w-50 d-none d-lg-block",
                ),
                # Links & Cart
                UL(
                    LI(
                        A(
                            "Products",
                            href=reverse("product:product-catalog"),
                            Class="nav-link",
                        ),
                        Class="nav-item",
                    ),
                    (
                        str()
                        if (user_status and not is_admin)
                        or not user_status
                        and not is_admin
                        else A(
                            "Dashboard",
                            href=reverse("cms:admin-dashboard", kwargs={}),
                            Class="nav-link",
                        )
                    ),
                    (
                        LI(
                            (
                                A(
                                    "Profile",
                                    href=reverse("client:profile_base", kwargs={}),
                                    Class="nav-link",
                                )
                            ),
                            Class="nav-item",
                        )
                        if user_status
                        else str()
                    ),
                    LI(
                        A(
                            "Logout" if user_status else "Log in",
                            href=(
                                reverse(
                                    f"client:login",
                                )
                                if not user_status
                                else "#"
                            ),
                            hx_post=(
                                reverse(
                                    f"client:logout",
                                )
                                if user_status
                                else False
                            ),
                            Class="nav-link",
                        ),
                        Class="nav-item",
                    ),
                    LI(
                        cart_icon(cart_count),
                        Class="nav-item ms-lg-3",
                    ),
                    Class="navbar-nav ms-auto align-items-center",
                ),
                Class="collapse navbar-collapse",
                id="navContent",
            ),
            Class="container",
        ),
        Class="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top",
    )

def ClientFooter() -> FOOTER:
    return FOOTER(
        DIV(
            DIV(
                DIV(
                    P(
                        "© 2026 Pythonic-Ecommerce. Built with Probo & Django.",
                        Class="text-muted mb-0",
                    ),
                    Class="col-md-6 text-center text-md-start",
                ),
                DIV(
                    A(
                        "Privacy Policy",
                        href="#",
                        Class="text-muted me-3 text-decoration-none",
                    ),
                    A(
                        "Terms of Service",
                        href="#",
                        Class="text-muted text-decoration-none",
                    ),
                    Class="col-md-6 text-center text-md-end",
                ),
                Class="row align-items-center",
            ),
            Class="container",
        ),
        Class="py-4 border-top mt-auto bg-light",
    )
# Class = "d-flex flex-column"
