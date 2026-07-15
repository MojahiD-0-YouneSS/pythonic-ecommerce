from django.urls import reverse

from probo import DIV, I, H4, P, A, SPAN, H5, BUTTON


def OrderDetailSection() -> DIV:
    """
    Renders detailed information about a specific order.
    """

    def order_detail_section(**dvars):
        order = dvars.get('order', {}) or {}
        if not order:
            return DIV(
                DIV(
                    I(Class="bi bi-exclamation-circle display-4 text-muted mb-3 d-block"),
                    H4("Order Not Found", Class="fw-bold"),
                    P("We couldn't find the details for this order.", Class="text-muted"),
                    A("Back to History", href="/client/profile/history/", Class="btn btn-primary mt-2"),
                    Class="text-center py-5",
                ),
                Class="card border-0 shadow-sm rounded-4 p-4",
            )

        status_color = 'success' if order.get('status') == 'Delivered' else 'warning text-dark'

        return DIV(
            DIV(
                # Header
                DIV(
                    DIV(
                        H4(f"Order #{order.get('id', '')}", Class="card-title fw-bold mb-0"),
                        SPAN(order.get("status", "Pending"), Class=f"badge bg-{status_color} ms-3"),
                        Class="d-flex align-items-center mb-3"
                    ),
                    A(I(Class="bi bi-arrow-left me-2"), "Back to History", href=reverse('order:order-history'),
                      Class="btn btn-sm btn-outline-secondary"),
                    Class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3"
                ),
                # Body
                DIV(
                    DIV(
                        H5("Order Information", Class="fw-bold mb-3"),
                        P(SPAN("Date: ", Class="text-muted"), SPAN(order.get('created_at', '-'), Class="fw-medium"),
                          Class="mb-2"),
                        P(SPAN("Total Amount: ", Class="text-muted"),
                          SPAN(f"${order.get('total_amount', '0.00')}", Class="fw-bold"), Class="mb-2"),
                        Class="col-md-6 mb-4"
                    ),
                    Class="row"
                ),
                Class="card border-0 shadow-sm rounded-4 p-4",
            )
        )

    return DIV(
        DIV(
            {'order',order_detail_section},
            Class="card-body p-4",
        ),
        Class="card border-0 shadow-sm rounded-4",
    )