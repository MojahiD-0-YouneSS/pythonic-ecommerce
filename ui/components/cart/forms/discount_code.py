from ui.components.shared.admin_form import AdminForm
from django.urls import reverse

def get_discount_form(*args,**kwargs):
    form = AdminForm()

    form.attr_manager.set_bulk_attr(
        hx_post=reverse("cart:admin_discount"),
        hx_target="#admin-form-container",
        hx_swap='innerHTML',
    )
    return form
