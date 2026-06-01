from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, SECTION, HR
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from ui.components.order.admin.helper_funnctions import get_status_badge, get_payment_badge

def OrderListRow(order):
    """
    Compact horizontal row for main table-style listing.
    """
    if order is None:
        return DIV(
            DIV(SPAN(f"#nothing to see here", Class="fw-bold"), Class="col-12"),
            Class="row align-items-center py-3 px-3 border-bottom hover-bg-light g-0"
        )

    username = order.user.user.username if hasattr(order, 'user') else "Guest"
    verified = getattr(order, 'verification', None)
    v_icon = I(Class="bi bi-patch-check-fill text-primary ms-1") if verified and verified.is_verified else ""

    return DIV(
        DIV(SPAN(f"#{order.id}", Class="fw-bold"), Class="col-1"),
        DIV(SPAN(username, Class="text-dark"), v_icon, Class="col-2"),
        DIV(SMALL(order.placed_at.strftime("%Y-%m-%d %H:%M"), Class="text-muted"), Class="col-2"),
        DIV(get_status_badge(order.status), Class="col-2"),
        DIV(SPAN(f"${order.total_amount}", Class="fw-bold"), Class="col-1"),
        DIV(get_payment_badge(order.payment_status), Class="col-2 text-center"),
        # DIV(
        #     A(I(Class="bi bi-pencil"), href=f"/admin/orders/edit/{order.id}/", Class="btn btn-xs btn-outline-secondary me-1"),
        #     BUTTON(I(Class="bi bi-three-dots"), Class="btn btn-xs btn-light"),
        #     Class="col-2 text-end"
        # ),
        Class="row align-items-center py-3 px-3 border-bottom hover-bg-light g-0"
    )
