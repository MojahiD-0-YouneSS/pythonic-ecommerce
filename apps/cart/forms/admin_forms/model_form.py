from ...models import (
    DiscountCode,
    Cart,
    CartItem
)
from django_abstract.base.base_form import BaseForm

class DiscountCodeForm(BaseForm):
    exclude_fields = ["uses", ]
    class Meta(BaseForm.Meta):
        model = DiscountCode

class CartForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Cart

class CartItemForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = CartItem
