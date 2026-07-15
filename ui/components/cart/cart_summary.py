from probo import DIV, H5, H6, P, BUTTON, HR,A
from decimal import Decimal
from django.urls import reverse
def CartSummaryCard():
    """The checkout summary card.
    {
    'cart': <Cart: Cart f529135f-3587-4095-b529-b25b950822ad (active)>,
    'cart_items': [<CartItem: Item Canvas Laptop Backpack 93C2 - SKU-019-RED-S-D7F9 in Cart f529135f-3587-4095-b529-b25b950822ad>, <CartItem: Item Canvas Laptop Backpack 93C2 - SKU-019-RED-M-1E26 in Cart f529135f-3587-4095-b529-b25b950822ad>, <CartItem: Item Canvas Laptop Backpack 93C2 - SKU-019-RED-L-20C5 in Cart f529135f-3587-4095-b529-b25b950822ad>, <CartItem: Item Canvas Laptop Backpack 93C2 - SKU-019-RED-E-0EFA in Cart f529135f-3587-4095-b529-b25b950822ad>],
    'sub_total_list': [Decimal('183.98'), Decimal('737.94'), Decimal('2167.92'), Decimal('632.97')],
    'cart_total': Decimal('3722.81'),
    """
    return DIV(
        DIV(
            H5("Order Summary", Class="fw-bold mb-4 mt-2 pt-1"),
            HR(Class="my-4"),
            # Subtotal Row
            DIV(
                H6("Items", Class="text-muted"),
                H6({"total_items"}),
                Class="d-flex justify-content-between mb-3",
            ),
            DIV(
                H6("Total Quantity", Class="text-muted"),
                H6({lambda **dvars:dvars.get("total_quantity", Decimal(0)),"total_quantity"}),
                Class="d-flex justify-content-between mb-3",
            ),
            DIV(
                H6("Subtotal", Class="text-muted"),
                H6({"cart_total",lambda **dvars:f"${dvars.get('cart_total',Decimal(0))}"}),
                Class="d-flex justify-content-between mb-3",
            ),
            # Shipping Row
            DIV(
                H6("Standard Shipping", Class="text-muted"),
                H6({lambda **dvars:f"${dvars.get('shipping_cost') or Decimal(5.00)}", "shipping_cost"}),
                Class="d-flex justify-content-between mb-3",
            ),
            HR(Class="my-4"),
            # Total Row
            DIV(
                H5("Total", Class="text-uppercase mb-3"),
                H5({lambda **dvars:f"${dvars.get('cart_total', Decimal(0))+(dvars.get('shipping_cost',)or Decimal(5.00))}", "shipping_cost", "cart_total"}),
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
        hx_swap_oob={"hx_oob",lambda **dvars:"true" if dvars.get('hx_oob',False) else False},
        Id=f"cart-summary",
    )
