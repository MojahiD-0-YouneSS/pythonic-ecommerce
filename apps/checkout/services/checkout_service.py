from django.db import transaction
from decimal import Decimal
from apps.cart.services.cart_service import CartModelService, DiscountCodeModelService
from apps.order.services.model_service import OrderModelService, OrderItemModelService
from django.core.exceptions import ValidationError
from django_abstract.base.base_service import BaseService
from apps.checkout.services.model_service import (
    CheckoutModelService,
    PaymentMethodModelService,
    OrderSummaryModelService,
)
from django_abstract.registry import register_service
from django_abstract.utilities import ServiceEntryData


@register_service()
class TaxService(BaseService):
    """
    Pure business logic for calculating taxes.
    Does NOT touch the database. Operates strictly in-memory.
    """

    hooks_list = []

    def __init__(self, session_key=None, **raw_data):
        super().__init__(session_key=session_key, **raw_data)
        self.validator = self.TaxValidator

    class TaxValidator(BaseService.BaseServiceValidator):

        def meta_hook(self):
            # 1. Define required inputs
            self.SERVICE_DOMAIN_FIELDS = ["price"]
            self.VALID_FIELDS_PER_ACTION = {"calculate_tax": ["price"]}
            # 2. Register the execution method
            self.regester_method("calculate_tax", self.calculate_tax)

        def calculate_tax(self):
            # 3. Extract inputs
            price = self.get_method_args("calculate_tax")[0]

            # Ensure safe decimal math
            if not isinstance(price, Decimal):
                price = Decimal(str(price))

            # 4. Pure Logic
            tax_rate = Decimal("0.10")  # 10%
            tax_amount = (price * tax_rate).quantize(Decimal("0.01"))

            # 5. Store outputs back into the Payload/State
            self.behavior.service_data.update(
                {
                    "tax_amount": tax_amount,
                    "tax_rate": tax_rate,
                    "price_with_tax": price + tax_amount,
                }
            )


@register_service()
class PricingService(BaseService):
    """Pure math logic for discounts and subtotals."""

    hooks_list = []

    def __init__(self, session_key=None, **raw_data):
        super().__init__(session_key=session_key, **raw_data)
        self.validator = self.PricingValidator

    class PricingValidator(BaseService.BaseServiceValidator):

        def meta_hook(self):
            self.SERVICE_DOMAIN_FIELDS = ["subtotal", "discount_pct"]
            self.VALID_FIELDS_PER_ACTION = {
                "calculate_discount": ["subtotal", "discount_pct"]
            }
            self.proxy_register()

        def proxy_register(self):
            self.regester_method("calculate_discount", self.calculate_discount)

        def calculate_discount(self):
            subtotal, discount_pct = self.get_method_args("calculate_discount")

            if not isinstance(subtotal, Decimal):
                subtotal = Decimal(str(subtotal))

            if not discount_pct or discount_pct <= 0:
                discount_amount = Decimal("0.00")
            else:
                discount_amount = subtotal * (
                    Decimal(str(discount_pct)) / Decimal("100")
                )

            discount_amount = discount_amount.quantize(Decimal("0.01"))

            self.behavior.service_data.update(
                {
                    "discount_amount": discount_amount,
                    "discounted_subtotal": subtotal - discount_amount,
                }
            )


@register_service()
class CheckoutOrchestrator(BaseService):
    """
    Coordinates the checkout process across Cart, Discount, Checkout, and Order domains.
    Wrapped in transaction.atomic so if one step fails, the whole database rolls back!
    """

    hooks_list = [
        "cart_model_service",
        "discount_code_model_service",
        "order_model_service",
        "order_item_model_service",
        "checkout_model_service",
        "tax_service",
        "pricing_service",
    ]

    def __init__(self, session_key, **kwargs):
        super().__init__(session_key=session_key, **kwargs)
        self.validator = self.CheckoutValidator

    class CheckoutValidator(BaseService.BaseServiceValidator):
        def meta_hook(self):
            self.SERVICE_DOMAIN_FIELDS = ["applied_discount_code","session_key"]
            self.VALID_FIELDS_PER_ACTION = {
                "process_checkout": ["applied_discount_code", "session_key"]
            }

            self.regester_method("process_checkout", self.process_checkout)

        @transaction.atomic
        def process_checkout(self):
            applied_discount_code, session_key = self.get_method_args(
                "process_checkout"
            )

            # --- 1. FETCH CART DATA ---
            # print('<********************************************************>')
            cart_svc = CartModelService(session_key=session_key, )
            entry = ServiceEntryData(service_data=(
                {"method_name": "get_cart", "session": session_key}
            ))
            cart_svc.hook(entry=entry)

            cart_data = cart_svc.entry.service_data
            cart_obj = cart_data.get("cart")
            cart_items = cart_data.get("cart_items", [])
            subtotal = Decimal(cart_data.get("cart_total", "0.00"))

            if not cart_items:
                raise ValidationError("Cannot checkout an empty cart.")

            # --- 2. HANDLE DISCOUNTS (Using Pure PricingService) ---
            discount_pct = Decimal("0.00")

            if applied_discount_code:
                discount_svc = DiscountCodeModelService(session_key=session_key)
                discount_svc.entry.service_data.update(
                    {"method_name": "get_discount_code", "pk": applied_discount_code}
                )
                discount_svc.hook()
                discount_pct = Decimal(
                    discount_svc.entry.service_data.get("discount_pct", "0.00")
                )

            # Execute Pricing Logic
            pricing_svc = PricingService(session_key=session_key)
            pricing_svc.entry.service_data.update(
                {
                    "method_name": "calculate_discount",
                    "subtotal": subtotal,
                    "discount_pct": discount_pct,
                }
            )
            pricing_svc.hook()

            discount_amount = pricing_svc.entry.service_data.get(
                "discount_amount", Decimal("0.00")
            )
            discounted_subtotal = pricing_svc.entry.service_data.get(
                "discounted_subtotal", subtotal
            )

            # --- 3. HANDLE TAXES (Using Pure TaxService) ---
            tax_svc = TaxService(session_key=session_key)
            tax_svc.entry.service_data.update(
                {"method_name": "calculate_tax", "price": discounted_subtotal}
            )
            tax_svc.hook()

            tax_amount = tax_svc.entry.service_data.get("tax_amount", Decimal("0.00"))
            final_total = tax_svc.entry.service_data.get(
                "price_with_tax", discounted_subtotal
            )

            # --- 5. CREATE THE ORDER ---
            order_svc = OrderModelService(
                session_key=session_key,
                load_record=False,
            )

            order_entry=ServiceEntryData(service_data=(
                {
                    "method_name": "create_entry",
                    "session_key": session_key,
                    "total_amount": final_total,
                    "status": "Pending",
                }
            ))
            order_svc.hook(entry=order_entry)
            new_order = order_svc.entry.raw_data.get("db_record")
            # --- 6. CREATE ORDER ITEMS ---
            for cart_item in cart_items:
                item_svc = OrderItemModelService(
                    session_key=session_key, auto_create=False
                )
                order_item_entry = ServiceEntryData(
                    service_data=(
                        {
                            "method_name": "add_order_item",
                            "order_id": new_order.id,
                            "product_variant_id": cart_item.product_variant.id,
                            "quantity": cart_item.quantity,
                            "price": cart_item.product_variant.base_price,
                        }
                    )
                )
                item_svc.hook(entry=order_item_entry)

            # --- 4. INITIATE CHECKOUT SESSION ---
            checkout_svc = CheckoutModelService(
                session_key=session_key,
            )
            checkout_entry = ServiceEntryData(
                service_data=(
                    {
                        "method_name": "initiate_checkout",
                        "session_key": session_key,
                        "cart_id": cart_obj.id,
                        "total_price": final_total,
                        "tax_amount": tax_amount,
                        "discount_amount": discount_amount,
                        "order_id": new_order.id,
                        "status": "initiated",
                    }
                )
            )
            checkout_obj = checkout_svc.hook(entry=checkout_entry)

            # --- 7. FINALIZE CHECKOUT AUDIT ---
            # Mark the checkout session as completed
            # checkout_svc.entry.service_data.update(
            #     {
            #         "method_name": "complete_checkout",
            #         "id": checkout_obj.id,
            #         "created_order_id": new_order.id,
            #     }
            # )
            # checkout_svc.hook()

            # Generate the financial summary snapshot
            summary_svc = OrderSummaryModelService(
                session_key=session_key, auto_create=True,load_record=False
            )
            summary_entry = ServiceEntryData(
                service_data=(
                    {
                        "method_name": "create_summary",
                        "checkout_id": checkout_obj.service_data.get("checkout").id,
                        "subtotal": subtotal,
                        "shipping_cost": Decimal("5.00"),  # Hardcoded for now
                        "notes": "Order arrives in 3 bussiness days",
                    }
                )
            )
            summary_svc.hook(entry=summary_entry)

            # Generate the payment attempt record
            payment_svc = PaymentMethodModelService(
                session_key=session_key, auto_create=True, load_record=False
            )
            payment_entry = ServiceEntryData(service_data=(
                {
                    "method_name": "add_payment",
                    "checkout_id": checkout_obj.service_data.get('checkout').id,
                    "provider": "stripe",  # Or whatever was passed from the UI
                    "amount_paid": final_total,
                }
            ))
            payment_svc.hook(entry=payment_entry)

            # --- 8. CLEAR THE CART ---
            cart_entry = ServiceEntryData(service_data=(
                {"method_name": "clear_cart", "session": session_key}
            ))
            cleared_cart_data = cart_svc.hook(entry=cart_entry)

            # --- 9. RETURN SUCCESS ---
            self.behavior.service_data["order"] = new_order
            self.behavior.service_data["checkout"] = checkout_obj.service_data.get('checkout')
            self.behavior.service_data.update(cleared_cart_data.service_data)
