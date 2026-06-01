from django_abstract.base.base_model import BaseModel, models, timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django_abstract.registry import creator_selector
from apps.order.dependencies import OrderAppDependency

@creator_selector(dependency=OrderAppDependency)
class Order(BaseModel):
    session_key = models.CharField(max_length=250)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Canceled', 'Canceled'),
            ('Returned', 'Returned'),
        ],
        default='Pending',
        verbose_name=_("Order Status")
    )
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ('Unpaid', 'Unpaid'),
            ('Paid', 'Paid'),
            ('Refunded', 'Refunded'),
        ],
        default='Unpaid',
        verbose_name=_("Payment Status")
    )
    tracking_number = models.CharField(max_length=50, blank=True, verbose_name=_("Tracking Number"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} - {self.session_key}"

@creator_selector(dependency=OrderAppDependency)
class OrderItem(BaseModel):
    """
    Represents a single line item within an Order.
    """

    # 1. The Order it belongs to
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="items",  # This allows you to do: order.items.all()
        verbose_name=_("Order"),
    )

    # 2. The Product/Variant purchased
    # (Adjust 'product.ProductVariant' to match your actual app and model name)
    product_variant = models.ForeignKey(
        "product.ProductVariant",
        on_delete=models.SET_NULL,
        null=True,  # We use SET_NULL so if you delete a product, past orders don't get deleted!
        related_name="order_items",
        verbose_name=_("Product Variant"),
    )

    # 3. The Details
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))

    # THE GOLDEN RULE: Snapshot the price at the exact moment of checkout!
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("The price of the item at the time of purchase."),
        verbose_name=_("Price at Purchase"),
    )

    def __str__(self):
        # Gracefully handle if a product was deleted from the database
        product_name = (
            self.product_variant.name if self.product_variant else "Deleted Product"
        )
        return f"{self.quantity}x {product_name} (Order {self.order.id if self.order else 'New'})"

    @property
    def subtotal(self):
        """Calculates the total for this specific line item"""
        if self.price and self.quantity:
            return self.price * self.quantity
        return 0

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        # Ensure we don't accidentally add the same exact variant twice to the same order.
        # (Though usually cart merging handles this, this is a good DB-level safety net)
        unique_together = ("order", "product_variant")

@creator_selector(dependency=OrderAppDependency)
class BillingAddress(BaseModel):
    session_key = models.CharField(max_length=250)
    full_name = models.CharField(max_length=150)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    delivery_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}, {self.address_line_1}, {self.city}"

@creator_selector(dependency=OrderAppDependency)
class ShippingAddress(BaseModel):
    session_key = models.CharField(max_length=250)
    full_name = models.CharField(max_length=150)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    delivery_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}, {self.address_line_1}, {self.city}"

@creator_selector(dependency=OrderAppDependency)
class OrderVerification(BaseModel):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='verification')
    method = models.CharField(max_length=50, choices=[('Email', 'Email'), ('SMS', 'SMS'), ('2FA', 'Two-Factor Authentication')])
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Verification for Order {self.order.id} - {'Verified' if self.is_verified else 'Pending'}"
