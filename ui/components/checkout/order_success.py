from decimal import Decimal
from probo import DIV, H2, H4, P, BUTTON, SPAN, I

def OrderSuccessReceipt():
    """The beautiful receipt shown after a successful transaction."""
    return DIV(
        DIV(
            I(Class="bi bi-check-circle-fill text-success", style="font-size: 4rem;"),
            H2("Payment Successful!", Class="fw-bold mt-3"),
            P(
                f"Thank you for your order. Your order number is ",
                SPAN({'order', lambda **dvars:f"#{getattr(dvars.get('order'),'id','')}"}, Class="fw-bold text-primary"),
                ".",
                Class="text-muted fs-5",
            ),
            Class="text-center mb-5",
        ),
        DIV(
            H4("Order Summary", Class="fw-bold border-bottom pb-2 mb-3"),
            DIV(
                SPAN("Total Paid:", Class="text-muted"),
                SPAN({'checkout', lambda **dvars:f"${getattr(dvars.get('checkout'),'total_price',Decimal(0))}"}, Class="fw-bold fs-4"),
                Class="d-flex justify-content-between align-items-center mb-2",
            ),
            DIV(
                SPAN("Status:", Class="text-muted"),
                SPAN({'order', lambda **dvars:getattr(dvars.get('order'),'get_status_display',lambda :'Pending')()}, Class="badge bg-success rounded-pill"),
                Class="d-flex justify-content-between align-items-center",
            ),
            Class="bg-light p-4 rounded-4 shadow-sm",
        ),
        # A button to go back shopping
        DIV(
            BUTTON(
                "Continue Shopping",
                Class="btn btn-outline-dark rounded-pill px-4 mt-4",
                onclick="window.location.href='/'",
            ),
            Class="text-center",
        ),
        Class="container py-5 animate__animated animate__fadeIn",
    )

