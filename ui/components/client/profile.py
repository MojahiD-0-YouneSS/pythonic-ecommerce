from probo import (
    DIV,
    H3,
    H4,
    P,
    FORM,
    INPUT,
    LABEL,
    BUTTON,
    TABLE,
    THEAD,
    TBODY,
    TR,
    TH,
    TD,
    SPAN,
    I,
    A,
    FIELDSET,
)
from django.urls import reverse

def ProfileInfoSection() -> DIV:
    """
    Renders the Personal Information form.
    Allows the user to update their name and phone number.
    """
    def profile_info_section(**dvars) -> FIELDSET:
        user = dvars.get('user_data',{}) or {}
        is_disabled = dvars.get('is_disabled',True)

        return FIELDSET(
                    DIV(
                        DIV(
                            LABEL("First Name", Class="form-label text-muted small"),
                            INPUT(
                                Type="text",
                                name="first_name",
                                value=user.get("first_name", ""),
                                Class="form-control",
                            ),
                            Class="col-md-6 mb-3",
                        ),
                        DIV(
                            LABEL("Last Name", Class="form-label text-muted small"),
                            INPUT(
                                Type="text",
                                name="last_name",
                                value=user.get("last_name", ""),
                                Class="form-control",
                            ),
                            Class="col-md-6 mb-3",
                        ),
                        Class="row",
                    ),
                    DIV(
                        LABEL("Email Address", Class="form-label text-muted small"),
                        INPUT(
                            Type="email",
                            value=user.get("email", ""),
                            Class="form-control bg-light",
                            readonly="true",
                        ),
                        P(
                            "Email addresses cannot be changed currently.",
                            Class="form-text text-muted small",
                        ),
                        Class="mb-3",
                    ),
                    DIV(
                        LABEL("Phone Number", Class="form-label text-muted small"),
                        INPUT(
                            Type="tel",
                            name="phone_number",
                            value=user.get("phone_number", ""),
                            Class="form-control",
                        ),
                        Class="mb-4",
                    ),
                    disabled=is_disabled,
                )
    return DIV(
        DIV(
            H4("Personal Information", Class="card-title fw-bold mb-4"),
            FORM(
                {'user','is_disabled',profile_info_section},
                BUTTON("Save Changes", Type="submit", Class="btn btn-dark px-4"),
                BUTTON(
                    "Edit Info",
                    Type="button",
                    Class="btn btn-warning px-4 ms-1",
                    hx_get=reverse("client:profile-info", kwargs={"is_disabled":0}),
                    hx_target="#profile-content-area",
                    hx_swap="innerHTML",
                ),
                # HTMX configuration to handle form submission without reloading
                hx_post=reverse("client:profile-info", kwargs={"is_disabled":0}),
                hx_target="#profile-content-area",
                hx_swap="innerHTML",
                disabled=True,
            ),
            Class="card-body p-4",
        ),
        Class="card border-0 shadow-sm rounded-4",
    )


def OrderHistorySection() -> DIV:
    """
    Renders the Order History table.
    """
    def order_history_section(**dvars):
        orders = dvars.get('orders',[]) or []
        if not orders:
            return DIV(
                DIV(
                    I(Class="bi bi-box-seam display-4 text-muted mb-3 d-block"),
                    H4("No orders yet", Class="fw-bold"),
                    P("When you place orders, they will appear here.", Class="text-muted"),
                    A("Start Shopping", href="/catalog/", Class="btn btn-primary mt-2"),
                    Class="text-center py-5",
                ),
                Class="card border-0 shadow-sm rounded-4 p-4",
            )

        order_rows = [
            TR(
                TD(SPAN(f"#{order.get('id', '')[:8]}", Class="font-monospace text-muted")),
                TD(order.get("created_at", "-")),
                TD(f"${order.get('total_amount', '0.00')}"),
                TD(
                    SPAN(
                        order.get("status", "Pending"),
                        Class=f"badge bg-{'success' if order.get('status') == 'Delivered' else 'warning text-dark'}",
                    )
                ),
                TD(
                    BUTTON(
                        "View Details",
                        hx_get=reverse('order:order_detail',kwargs={'order_id':order.get('id')}),
                        hx_target="#profile-content-area",
                        hx_swap="innerHTML",
                        Class="btn btn-sm btn-outline-dark",
                    )
                ),
                Class="align-middle",
            )
            for order in orders
        ]
        return TBODY(*order_rows)
    return DIV(
        DIV(
            H4("Order History", Class="card-title fw-bold mb-4"),
            TABLE(
                THEAD(
                    TR(
                        TH("Order ID"),
                        TH("Date"),
                        TH("Total"),
                        TH("Status"),
                        TH("Action"),
                        Class="text-muted small border-bottom",
                    )
                ),
                {'orders',order_history_section},
                Class="table table-hover align-middle mb-0",
            ),
            Class="card border-0 shadow-sm rounded-4 p-4",
        )
    )

def AddressBookSection() -> DIV:
    """
    Renders a grid of saved addresses.
    """
    def address_book_section(**dvars):
        addresses: list|None = dvars.get('addresses',None)
        shipping_addresses = dvars.get('shipping_addresses',None)
        address_cards = []
        if addresses:
            for addr in addresses:
                address_cards.append(
                    DIV(
                        DIV(
                            DIV(
                                H4(
                                    "Default" if addr.get("is_default") else "Address",
                                    Class=f"badge {'bg-primary' if addr.get('is_default') else 'bg-secondary'} mb-2",
                                ),
                                P(addr.get("street_address", ""), Class="mb-1 fw-medium"),
                                P(
                                    f"{addr.get('city', '')}, {addr.get('state', '')} {addr.get('zip_code', '')}",
                                    Class="text-muted small mb-0",
                                ),
                                P(addr.get("country", ""), Class="text-muted small mb-3"),
                                DIV(
                                    BUTTON(
                                        "Edit",
                                        Class="btn btn-sm btn-outline-secondary me-2",
                                    ),
                                    BUTTON("Delete", Class="btn btn-sm btn-outline-danger"),
                                    BUTTON("Set as Shipping", Class="btn btn-sm btn-outline-primary ms-2"),
                                    Class="mt-auto",
                                ),
                                Class="card-body d-flex flex-column",
                            ),
                            Class="card h-100 border shadow-sm rounded-3",
                        ),
                        Class="col-md-6 mb-4",
                    )
                )
            return DIV(*address_cards, Class="row")
        else:

            return DIV(
                    P("You haven't saved any addresses yet.", Class="text-muted my-4"),
                    Class="col-12 text-center",
                )


    return DIV(
        DIV(
            DIV(
                H4("Address Book", Class="card-title fw-bold m-0"),
                BUTTON(
                    I(Class="bi bi-plus-lg me-1"),
                    "Add New Address",
                    Class="btn btn-dark btn-sm rounded-pill px-3",
                    hx_get=reverse("order:add-billing-address"),
                    hx_target="#profile-content-area",
                    hx_swap="innerHTML",
                ),
                Class="d-flex justify-content-between align-items-center mb-4",
            ),
            {'addresses','shipping_addresses',address_book_section},
            Class="card-body p-4",
        ),
        Class="card border-0 shadow-sm rounded-4",
    )


def SecuritySection() -> DIV:
    """
    Renders the password update form.
    """
    def security_section(**dvars):
        user_data = dvars.get('user_data', None)
        is_disabled = dvars.get('is_disabled', True)
        error = dvars.get('error', None)

        return FIELDSET(
                    DIV(
                        LABEL("Current Password", Class="form-label text-muted small"),
                        INPUT(
                            Type="password",
                            name="current_password",
                            value="",
                            Class="form-control",
                        ),
                        P(error, Class="text-danger small") if error else str(),
                        Class="mb-3",
                    ),
                    DIV(
                        LABEL("New Password", Class="form-label text-muted small"),
                        INPUT(
                            Type="password",
                            name="new_password",
                            value= "",
                            Class="form-control",
                            required=True,
                        ),
                        Class="mb-3",

                    ),
                    DIV(
                        LABEL(
                            "Confirm New Password", Class="form-label text-muted small"
                        ),
                        INPUT(
                            Type="password",
                            name="confirmed_password",
                            value= "",
                            Class="form-control",
                            required=True,
                        ),
                        Class="mb-4",
                    ),
                    disabled=bool(is_disabled),
                )
    return DIV(
        DIV(
            H4("Security & Password", Class="card-title fw-bold mb-4"),
            FORM(
                {'user_data','is_disabled','error',security_section},
                BUTTON(
                    "Update Password",
                    Type="submit",
                    Class="btn btn-danger px-4",
                ),
                BUTTON(
                    "Edit Password",
                    Type="button",
                    Class="btn btn-primary px-4 ms-2",
                    hx_get=reverse("client:profile-login", kwargs={"is_disabled": 0}),
                    hx_target="#profile-content-area",
                    hx_swap="innerHTML",
                ),
                BUTTON(
                    "Discard Changes",
                    Type="button",
                    Class="btn btn-secondary px-4 ms-2",
                    hx_get=reverse("client:profile-login-default"),
                    hx_target="#profile-content-area",
                    hx_swap="innerHTML",
                ),
                hx_post=reverse("client:profile-login-default"),
                hx_target="#profile-content-area",
                hx_swap="innerHTML",
            ),
            Class="card-body p-4",
        ),
        Class="card border-0 shadow-sm rounded-4",
    )


def ClientProfile():
    """
    The master layout for the profile page.
    The left sidebar controls navigation. The right side swaps content via HTMX.
    """
    def active_tab_html(**dvars):
        active_html = dvars.get('active_tab_html')
        return DIV(
                # This inner HTML gets replaced when sidebar links are clicked!
                active_html,
                Id="profile-content-area",
                Class="col-md-9",
            )
    return DIV(
        DIV(
            # --- LEFT SIDEBAR ---
            DIV(
                DIV(
                    A(
                        I(Class="bi bi-person me-2"),
                        "Personal Info",
                        href="#",
                        # HTMX attributes for instant tab switching
                        hx_get=reverse("client:profile-info-default"),
                        hx_target="#profile-content-area",
                        hx_swap="innerHTML",
                        Class="list-group-item list-group-item-action active",
                    ),
                    A(
                        I(Class="bi bi-box me-2"),
                        "Order History",
                        href="#",
                        hx_get=reverse("order:order-history"),
                        hx_target="#profile-content-area",
                        hx_swap="innerHTML",
                        Class="list-group-item list-group-item-action",
                    ),
                    A(
                        I(Class="bi bi-geo-alt me-2"),
                        "Addresses",
                        href="#",
                        hx_get=reverse("order:billing-address"),
                        hx_target="#profile-content-area",
                        hx_swap="innerHTML",
                        Class="list-group-item list-group-item-action",
                    ),
                    A(
                        I(Class="bi bi-shield-lock me-2"),
                        "Security",
                        href="#",
                        hx_get=reverse("client:profile-login-default"),
                        hx_target="#profile-content-area",
                        hx_swap="innerHTML",
                        Class="list-group-item list-group-item-action",
                    ),
                    Class="list-group list-group-flush shadow-sm rounded",
                ),
                Class="col-md-3 mb-4",
            ),
            # --- RIGHT CONTENT AREA (HTMX TARGET) ---
            {'active_tab_html',active_tab_html},
            Class="row mt-5",
        ),
        Class="container",
    )
