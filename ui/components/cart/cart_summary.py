from probo import DIV, H5, H6, P, BUTTON, HR,A
from apps.global_context import get_global_context
from decimal import Decimal
from django.urls import reverse
def CartSummaryCard(cart, hx_oob=False):
    """The checkout summary card."""
    ctx = get_global_context()
    subtotal = ctx.get("cart_total", Decimal(0))
    item_count = ctx.get("total_items", Decimal(0))
    total_quantity = ctx.get("total_quantity", Decimal(0))
    shipping_cost = ctx.get("shipping_cost", Decimal(5.00))
    return DIV(
        DIV(
            H5("Order Summary", Class="fw-bold mb-4 mt-2 pt-1"),
            HR(Class="my-4"),
            # Subtotal Row
            DIV(
                H6("Items", Class="text-muted"),
                H6(item_count),
                Class="d-flex justify-content-between mb-3",
            ),
            DIV(
                H6("Total Quantity", Class="text-muted"),
                H6(total_quantity),
                Class="d-flex justify-content-between mb-3",
            ),
            DIV(
                H6("Subtotal", Class="text-muted"),
                H6(f"${subtotal}"),
                Class="d-flex justify-content-between mb-3",
            ),
            # Shipping Row
            DIV(
                H6("Standard Shipping", Class="text-muted"),
                H6(f"${shipping_cost}"),
                Class="d-flex justify-content-between mb-3",
            ),
            HR(Class="my-4"),
            # Total Row
            DIV(
                H5("Total", Class="text-uppercase mb-3"),
                H5(f"${subtotal + shipping_cost}"),
                Class="d-flex justify-content-between mb-5",
            ),
            # Checkout Button
            A(
                "Proceed to Checkout",
                hx_post=reverse("checkout:process_checkout"),
                hx_target='#checkou-modal',
                hx_swap='innerHTML',
                Class="btn btn-dark btn-block btn-lg w-100",
            ),
            Class="p-5",
        ),
        Class="card bg-light rounded-3",
        hx_swap_oob="true" if hx_oob else False,
        Id=f"cart-summary",
    )
