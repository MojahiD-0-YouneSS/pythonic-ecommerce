from django_abstract.base.base_form import BaseForm 
from apps.order.models import (
    BillingAddress,
    ShippingAddress,
)

class BillingAddressModelForm(BaseForm):
    exclude_fields = ['session_key']
    class Meta(BaseForm.Meta):
        model= BillingAddress
class ShippingAddressModelForm(BaseForm):
    class Meta(BaseForm.Meta):
        model= ShippingAddress
