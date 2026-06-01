from django_abstract.base.base_model import BaseModel, models, timezone
from apps.checkout.dependencies import CheckoutAppDependency
from django_abstract.registry import creator_selector

@creator_selector(dependency=CheckoutAppDependency)
class Checkout(BaseModel):
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, related_name='checkouts')
    created_order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='checkouts')
    session_key = models.CharField(max_length=250, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('initiated', 'Initiated'), ('completed', 'Completed'), ('abandoned', 'Abandoned')])
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Checkout {self.id} - Status: {self.status}"


@creator_selector(dependency=CheckoutAppDependency)
class OrderSummary(BaseModel):
    """Snapshot of the financial breakdown for display and historical tracking."""

    checkout = models.OneToOneField(
        "Checkout", on_delete=models.CASCADE, related_name="summary"
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(
        blank=True, null=True, help_text="Special instructions from the customer."
    )

    def __str__(self):
        return f"Summary for Checkout {self.checkout.id}"

@creator_selector(dependency=CheckoutAppDependency)
class PaymentMethod(BaseModel):
    """Tracks the payment gateway transaction (Stripe, PayPal, COD)."""

    checkout = models.ForeignKey(
        "Checkout", on_delete=models.CASCADE, related_name="payments"
    )
    provider = models.CharField(
        max_length=50,
        choices=[
            ("stripe", "Stripe"),
            ("paypal", "PayPal"),
            ("cod", "Cash on Delivery"),
        ],
    )
    transaction_id = models.CharField(
        max_length=150, blank=True, null=True, help_text="Stripe/PayPal intent ID"
    )
    is_successful = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.provider} - Checkout {self.checkout.id}"
