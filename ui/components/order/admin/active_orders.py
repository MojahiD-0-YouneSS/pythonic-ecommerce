from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, SECTION, HR
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from ui.components.order.admin.helper_funnctions import get_status_badge, get_payment_badge

def ActiveOrderCard(order):
    """
    Focused card for orders currently being handled (Pending/Processing).
    """
    username = order.user.user.username if hasattr(order, 'user') else "Guest"
    
    return DIV(
        DIV(
            DIV(
                H6(f"#{order.id}", Class="mb-0 fw-bold"),
                SMALL(order.placed_at.strftime("%H:%M - %d %b"), Class="text-muted"),
                Class="flex-grow-1"
            ),
            get_status_badge(order.status),
            Class="d-flex align-items-center mb-3"
        ),
        DIV(
            I(Class="bi bi-person me-2 text-muted"),
            SPAN(username, Class="small text-dark fw-medium"),
            Class="mb-2"
        ),
        DIV(
            I(Class="bi bi-currency-dollar me-2 text-muted"),
            SPAN(f"${order.total_amount}", Class="fw-bold text-primary"),
            get_payment_badge(order.payment_status),
            Class="d-flex align-items-center justify-content-between mb-3"
        ),
        DIV(
            A("Manage Order", href=reverse("order:admin_order_management", kwargs={"order_id": order.id}), Class="btn btn-sm btn-outline-primary w-100"),
            Class="border-top pt-2"
        ),
        Class="card shadow-sm p-3 mb-3 border-0",
        style="width: 280px; border-left: 4px solid #ffc107 !important;" if order.status == 'Pending' else "width: 280px;"
    )
