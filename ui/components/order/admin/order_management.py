from django.urls import reverse
from probo import (
    DIV,
    H4,
    H5,
    H6,
    P,
    SPAN,
    I,
    BUTTON,
    A,
    TABLE,
    THEAD,
    TBODY,
    TR,
    TH,
    TD,
    FORM,
    SELECT,
    OPTION,
    LABEL,
    HR,
    INPUT,
    
)


def OrderManagementSection(order) -> DIV:
    """
    The detailed management view for a specific order.
    Perfectly mapped to the actual Order, OrderItem, and Address models.
    """
    if not order:
        return DIV("Order not found.", Class="alert alert-danger m-4")

    # Helper function to generate dropdown options
    def generate_options(current_val, choices):
        return [
            OPTION(label, value=val, selected="true" if current_val == val else None)
            for val, label in choices
        ]

    # Safe extraction of related models (they have null=True)
    shipping = getattr(order, "shipping_address", None)
    billing = getattr(order, "billing_address", None)

    # Customer identifier fallback
    customer_name = (
        shipping.full_name
        if shipping
        else billing.full_name if billing else order.session_key[:8]
    )
    customer_phone = (
        shipping.phone_number
        if shipping
        else billing.phone_number if billing else "N/A"
    )

    # --- 1. LEFT COLUMN: Items & Pricing ---
    items_rows = []
    subtotal = 0

    # Iterate through the actual OrderItem model queryset
    for item in order.items.all():
        product_name = (
            item.product_variant.product.name
            if item.product_variant
            else "Deleted Product"
        )
        sku = item.product_variant.sku if item.product_variant else "N/A"
        item_subtotal = item.subtotal
        subtotal += item_subtotal

        items_rows.append(
            TR(
                TD(
                    P(product_name, Class="fw-bold mb-0 text-dark"),
                    P(f"SKU: {sku}", Class="text-muted small mb-0"),
                ),
                TD(f"${item.price}", Class="text-center align-middle"),
                TD(f"x{item.quantity}", Class="text-center align-middle"),
                TD(f"${item_subtotal}", Class="text-end fw-bold align-middle"),
                Class="align-middle",
            )
        )

    left_column = DIV(
        # Items Card
        DIV(
            DIV(
                H5("Order Items", Class="card-title fw-bold m-0"),
                Class="card-header bg-white border-bottom-0 pt-4 pb-0 px-4",
            ),
            DIV(
                TABLE(
                    THEAD(
                        TR(
                            TH(
                                "Product",
                                Class="text-muted small text-uppercase border-0",
                            ),
                            TH(
                                "Price",
                                Class="text-center text-muted small text-uppercase border-0",
                            ),
                            TH(
                                "Qty",
                                Class="text-center text-muted small text-uppercase border-0",
                            ),
                            TH(
                                "Total",
                                Class="text-end text-muted small text-uppercase border-0",
                            ),
                        ),
                        Class="table-light",
                    ),
                    (
                        TBODY(*items_rows)
                        if items_rows
                        else TBODY(
                            TR(
                                TD(
                                    "No items found.",
                                    colspan="4",
                                    Class="text-center text-muted py-4",
                                )
                            )
                        )
                    ),
                    Class="table mb-0",
                ),
                Class="table-responsive px-2",
            ),
            # Pricing Summary inside the same card
            DIV(
                DIV(
                    SPAN("Subtotal", Class="text-muted"),
                    SPAN(f"${subtotal:.2f}", Class="fw-medium"),
                    Class="d-flex justify-content-between mb-2",
                ),
                (
                    DIV(
                        SPAN("Discount", Class="text-muted"),
                        SPAN(f"-${order.discount}", Class="fw-medium text-success"),
                        Class="d-flex justify-content-between mb-3",
                    )
                    if order.discount > 0
                    else ""
                ),
                HR(Class="my-2"),
                DIV(
                    SPAN("Total Amount", Class="fw-bold fs-5"),
                    SPAN(f"${order.total_amount}", Class="fw-bold fs-5 text-primary"),
                    Class="d-flex justify-content-between mt-2",
                ),
                Class="card-body bg-light rounded-bottom-4 p-4 border-top",
            ),
            Class="card border-0 shadow-sm rounded-4 mb-4",
        ),
        Class="col-lg-8",
    )

    # --- 2. RIGHT COLUMN: Control Panel & Customer Info ---
    right_column = DIV(
        # --- ACTION CONTROL PANEL ---
        DIV(
            DIV(
                H5(
                    I(Class="bi bi-sliders me-2"),
                    "Process Order",
                    Class="card-title fw-bold mb-3",
                ),
                FORM(
                    # Payment Status Toggle
                    DIV(
                        LABEL(
                            "Payment Status",
                            Class="form-label fw-bold small text-muted mb-1",
                        ),
                        SELECT(
                            *generate_options(
                                order.payment_status,
                                [
                                    ("Unpaid", "Unpaid"),
                                    ("Paid", "Paid (Captured)"),
                                    ("Refunded", "Refunded"),
                                ],
                            ),
                            name="payment_status",
                            Class=f"form-select fw-medium {'border-danger text-danger' if order.payment_status == 'Unpaid' else 'border-success text-success'}",
                            required=True,
                        ),
                        Class="mb-3",
                    ),
                    # Order/Delivery Status Toggle
                    DIV(
                        LABEL(
                            "Order Status",
                            Class="form-label fw-bold small text-muted mb-1",
                        ),
                        SELECT(
                            *generate_options(
                                order.status,
                                [
                                    ("Pending", "Pending"),
                                    ("Processing", "Processing"),
                                    ("Shipped", "Shipped"),
                                    ("Delivered", "Delivered"),
                                    ("Canceled", "Canceled"),
                                    ("Returned", "Returned"),
                                ],
                            ),
                            name="status",
                            Class="form-select fw-medium bg-light",
                            required=True,
                        ),
                        Class="mb-3",
                    ),
                    # Tracking Number Input
                    DIV(
                        LABEL(
                            "Tracking Number",
                            Class="form-label fw-bold small text-muted mb-1",
                        ),
                        INPUT(
                            Type="text",
                            name="tracking_number",
                            value=order.tracking_number,
                            placeholder="e.g., 1Z9999999999999999",
                            Class="form-control",
                            required=True,
                        ),
                        Class="mb-4",
                    ),
                    # Update Button
                    BUTTON(
                        "Save Changes",
                        Type="submit",
                        Class="btn btn-primary w-100 fw-bold",
                        # HTMX posts the new statuses and re-renders this component
                    ),
                        hx_post=reverse("order:admin_order_processing", kwargs={"order_id": order.id}),
                        hx_target="#order-processing-form",
                        hx_swap="outerHTML",
                    # method="POST",
                ),
                Class="card-body p-4",
                Id="order-processing-form",
            ),
            Class="card border-primary shadow-sm rounded-4 mb-4 border-2",
        ),
        # --- CUSTOMER INFO CARD ---
        DIV(
            DIV(
                H6("Customer Details", Class="fw-bold mb-3"),
                DIV(
                    I(Class="bi bi-person me-2 text-muted"),
                    SPAN(customer_name),
                    Class="mb-2",
                ),
                DIV(
                    I(Class="bi bi-telephone me-2 text-muted"),
                    SPAN(customer_phone),
                    Class="mb-0",
                ),
                HR(Class="my-3"),
                H6("Shipping Address", Class="fw-bold mb-2"),
                # Format the actual ShippingAddress model
                DIV(
                    (
                        P(shipping.address_line_1, Class="mb-0 small text-muted")
                        if shipping
                        else P("No address provided.", Class="mb-0 small text-muted")
                    ),
                    (
                        P(shipping.address_line_2, Class="mb-0 small text-muted")
                        if shipping and shipping.address_line_2
                        else ""
                    ),
                    (
                        P(
                            f"{shipping.city}, {shipping.state} {shipping.postal_code}",
                            Class="mb-0 small text-muted",
                        )
                        if shipping
                        else ""
                    ),
                    (
                        P(shipping.country, Class="mb-0 small text-muted")
                        if shipping
                        else ""
                    ),
                    # Show delivery instructions if they exist
                    (
                        DIV(
                            P(
                                "Instructions:",
                                Class="fw-bold text-dark mb-0 mt-2",
                                style="font-size: 0.75rem;",
                            ),
                            P(
                                shipping.delivery_instructions,
                                Class="text-muted fst-italic mb-0",
                                style="font-size: 0.75rem;",
                            ),
                        )
                        if shipping and shipping.delivery_instructions
                        else ""
                    ),
                ),
                Class="card-body p-4",
            ),
            Class="card border-0 shadow-sm rounded-4",
        ),
        Class="col-lg-4",
    )

    # --- IDENTIFY VERIFICATION STATUS ---
    verification_badge = ""
    if hasattr(order, "verification") and order.verification:
        if order.verification.is_verified:
            verification_badge = SPAN(
                I(Class="bi bi-shield-check me-1"),
                "Verified",
                Class="badge bg-success ms-3",
            )
        else:
            verification_badge = SPAN(
                I(Class="bi bi-shield-exclamation me-1"),
                "Unverified",
                Class="badge bg-warning text-dark ms-3",
            )

    # --- MAIN PAGE ASSEMBLY ---
    return DIV(
        # Header Row
        DIV(
            DIV(
                BUTTON(
                    I(Class="bi bi-arrow-left me-1"),
                    "Back to Orders",
                    Class="btn btn-sm btn-light text-muted fw-medium mb-3",
                    hx_get="/custom-admin/orders/",
                    hx_target="#admin-content-area",
                    hx_swap="innerHTML",
                ),
                DIV(
                    H4(f"Order #{order.id}", Class="fw-bold m-0 d-inline-block"),
                    verification_badge,
                    Class="d-flex align-items-center mb-1",
                ),
                P(
                    (
                        order.placed_at.strftime("%b %d, %Y - %H:%M")
                        if order.placed_at
                        else "Unknown Date"
                    ),
                    Class="text-muted small m-0",
                ),
            ),
            Class="d-flex justify-content-between align-items-end mb-4",
        ),
        # Two-Column Grid
        DIV(left_column, right_column, Class="row"),
    )
