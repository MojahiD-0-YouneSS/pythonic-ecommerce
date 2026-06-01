from probo import DIV, H2, H4, P, BUTTON, SPAN, I, FORM, INPUT


def CheckoutForm(subtotal=0, has_items=True):
    """The final form/button to trigger the checkout process."""
    if not has_items:
        return DIV(
            P("Your cart is empty.", Class="text-muted"), Class="text-center p-4"
        )

    return FORM(
        # Optional: Hidden input if you want to pass a discount code from the UI
        INPUT(
            type="hidden", name="discount_code", value="", id="applied_discount_input"
        ),
        BUTTON(
            I(Class="bi bi-lock-fill me-2"),
            "Secure Checkout",
            type="submit",
            Class="btn btn-primary btn-lg w-100 rounded-pill shadow-sm fw-bold mt-3",
        ),
        # HTMX config: POST to the checkout endpoint and replace this container
        hx_post="/checkout/api/process/",
        hx_target="#checkout-wrapper",
        hx_swap="innerHTML",
        hx_indicator="#checkout-spinner",  # Optional: shows a spinner while processing
        id="checkout-form",
        Class="mt-4",
    )
