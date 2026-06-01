from apps.cart.forms.admin_forms.model_form import (
    DiscountCodeForm,
    CartForm,
    CartItemForm,
)
from ui.components.shared.admin_form import AdminForm
from django.urls import reverse

def get_discout_form(*args,**kwargs):
    rdt = kwargs.get('rdt',None)
    form = AdminForm(
        rdt.form if rdt.errors else rdt.form_class(),
        action="#",
        hx_post=reverse("cart:admin_discount"),
        hx_target="#admin-form-container",
        hx_swap='innerHTML',
    )
    return form
