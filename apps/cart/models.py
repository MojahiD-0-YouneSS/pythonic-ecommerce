from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django_abstract.base.base_model import BaseModel, models, timezone
from .dependencies import CartAppDependency
from django_abstract.registry import creator_selector

@creator_selector(dependency=CartAppDependency)
class Cart(BaseModel):
    session = models.CharField(max_length=250, unique=True, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('abandoned', 'Abandoned'), ('completed', 'Completed')], default='active')
    products = models.ManyToManyField('product.ProductVariant', through='CartItem')
    item_count = models.PositiveIntegerField(default=0)
    is_checked_out = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Cart {self.id} ({self.status})"
    def get_subtotal(self,):
        return 0
@creator_selector(dependency=CartAppDependency)
class CartItem(BaseModel):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"Item {self.product_variant} in Cart {self.cart.id}"

@creator_selector(dependency=CartAppDependency)
class DiscountCode(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(
        max_length=10,
        choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')]
    )
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_uses = models.PositiveIntegerField(default=0)
    uses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Discount Code {self.code} ({self.discount_percentage}%)"
