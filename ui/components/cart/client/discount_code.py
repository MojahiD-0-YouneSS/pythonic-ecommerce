from probo import DIV, H4, P, BUTTON, SPAN, I 
from django.urls import reverse
from probo.components import Frag
def DiscountCode() -> Frag:
    """
    Renders the interactive coupon section.
    If 'code' is None, shows the HTMX button.
    If 'code' is provided, shows the revealed discount code.
    """
    def process_code(**dvars)->DIV:
        code = dvars.get('code',None)
        if code:
         return DIV(
             H4("🎉 Here is your coupon!", Class="text-success fw-bold"),
        P(
            "Use this code at checkout to get your discount.",
            Class="text-muted mb-3",
        ),
        DIV(
            SPAN(
                code,
                Class="fs-3 fw-bold text-dark font-monospace me-3 letter-spacing-1",
            ),
            # A little vanilla JS to copy the code to the clipboard!
            BUTTON(
                I(Class="bi bi-clipboard me-1"),
                "Copy",
                Class="btn btn-sm btn-outline-success rounded-pill px-3",
                onclick=f"navigator.clipboard.writeText('{code}'); alert('Copied!');",
            ),
            Class="d-inline-flex align-items-center bg-light p-3 rounded-3 border border-success border-dashed",
        ),
        id = "coupon-container",  # MUST match the original ID so HTMX swaps correctly
        Class = "mt-4 p-4 border border-success rounded-4 shadow-sm bg-white text-center transition-all",

    )
        else:
    # STATE 1: The initial button
            return DIV(
                H4("🎁 Special Offer", Class="fw-bold"),
                P(
                    "Click the button below to reveal your exclusive discount code!",
                    Class="text-muted",
                ),
                BUTTON(
                    I(Class="bi bi-gift-fill me-2"),
                    "Get the Coupon",
                    Class="btn btn-dark btn-lg rounded-pill px-4 shadow-sm",
                    # HTMX Magic:
                    hx_get=reverse("cart:discount"),  # The URL to hit
                    hx_target="#coupon-container",  # The element to replace
                    hx_swap="outerHTML",  # Replace the whole container
                ),
                id="coupon-container",
                Class="mt-4 p-4 border rounded-4 shadow-sm bg-light text-center",
            )
    return Frag({'code',process_code})
