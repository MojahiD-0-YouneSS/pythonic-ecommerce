from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, SECTION, HR
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from ui.components.order.admin.helper_funnctions import get_status_badge, get_payment_badge

def ReadyToDeliverCard():
    """
    Action-oriented card for orders that are paid and ready for shipment.
    """


    return DIV(
        DIV(
            I(Class="bi bi-truck fs-4 text-success me-3"),
            DIV(
                H6({'order',lambda **dvars:f"Order #{getattr(dvars.get('order'),'id',0)}"}, Class="mb-0"),
                SMALL({'order',lambda **dvars:f"{dvars.get('order').shipping_address.city}, {dvars.get('order').shipping_address.country}" if getattr(dvars.get('order'),'shipping_address',None) else "Address Missing"}, Class="text-muted"),
                Class="flex-grow-1"
            ),
            Class="d-flex align-items-center mb-3"
        ),
        P({'order',lambda **dvars:f"Items Total: ${getattr(dvars.get('order'),'shipping_address',0)}"},  Class="small mb-3 fw-bold"),
        DIV(
            BUTTON(I(Class="bi bi-box-seam me-1"), "Ship Now", 
                   Class="btn btn-sm btn-success flex-fill me-2",
                   hx_post=f"#"),
            A(I(Class="bi bi-printer"), href=f"#", 
              Class="btn btn-sm btn-outline-secondary", target="_blank"),
            Class="d-flex"
        ),
        Class="card shadow-sm p-3 mb-3 border-0 bg-light-success",
        style="width: 320px; border-bottom: 3px solid #198754 !important;"
    )
