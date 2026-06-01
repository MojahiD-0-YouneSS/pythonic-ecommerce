from django_abstract.base.base_model_service import BaseModelService
from apps.checkout.dependencies import CheckoutAppDependency
from django.utils import timezone
from django_abstract.registry import register_service

@register_service()
class CheckoutModelService(BaseModelService):
    model_dependency = CheckoutAppDependency()
    model_slug = "checkout"

    def __init__(self, session_key, *args, auto_create=False, **db_fields):
        # We map include_session_key_as="session_key" because your model named the field 'user'
        super().__init__(
            session_key=session_key,
            *args,
            include_session=True,
            auto_create=auto_create,
            load_record=False,
            **db_fields
        )
        self.validator = self.CheckoutValidator
        self.init_state_hook()

    class CheckoutValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            # We use 'user' (session_key) or 'id' to find the checkout
            self.MINIMUM_READ_FIELDS = ["session_key"]
            self.MINIMUM_WRITE_FIELDS = ["session_key", "cart", "created_order"]
            self.SERVICE_DOMAIN_FIELDS = [
                "session_key",
                "cart",
                "cart_id",
                "order_id",
                "created_order",
                "total_price",
                "tax_amount",
                "discount_amount",
                "status",
                "pk",
            ]

            self.VALID_FIELDS_PER_ACTION = {
                "initiate_checkout": [
                    "session_key",
                    "cart_id",
                    "order_id",
                    "total_price",
                    "tax_amount",
                    "discount_amount",
                    "status",
                ],
                
                "complete_checkout": ["pk", "order_id"],
                "abandon_checkout": ["pk"],
            }

            self.set_db_methods_fields("read_entry", "session_key")
            self.set_db_methods_fields("delete_entry", "id")
            self.set_db_methods_fields(
                "create_entry", "session_key", "cart_id", "total_price"
            )

            self.regester_method("initiate_checkout", self.initiate_checkout)
            self.regester_method("complete_checkout", self.complete_checkout)
            self.regester_method("abandon_checkout", self.abandon_checkout)

        def initiate_checkout(self):
            session_key, cart_id, order_id, total_price, tax_amount, discount_amount, status = (
                self.get_method_args("initiate_checkout")
            )
            checkout = self.parent_service.access_db_objects.create(
                session_key=session_key,
                cart_id=cart_id,
                created_order_id=order_id,
                total_price=total_price,
                tax_amount=tax_amount,
                discount_amount=discount_amount,
                status=status or "initiated",
            )
            self.behavior.service_data.update({"checkout": checkout})

        def complete_checkout(self):
            checkout_id, created_order_id = self.get_method_args("complete_checkout")
            checkout = self.parent_service.db_record

            if checkout:
                checkout.status = "completed"
                checkout.created_order_id = created_order_id
                checkout.completed_at = timezone.now()
                checkout.save()
                self.behavior.service_data.update({"checkout": checkout})

        def abandon_checkout(self):
            checkout_id = self.get_method_args("abandon_checkout")[0]
            checkout = self.parent_service.db_record

            if checkout and checkout.status == "initiated":
                checkout.status = "abandoned"
                checkout.save()
                self.behavior.service_data.update({"checkout": checkout})


@register_service()
class PaymentMethodModelService(BaseModelService):
    model_dependency = CheckoutAppDependency()
    model_slug = "payment_method"

    def __init__(self, session_key, *args, **db_fields):
        super().__init__(
            session_key=session_key, *args, include_session=False, **db_fields
        )
        self.validator = self.PaymentValidator
        self.init_state_hook()

    class PaymentValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.MINIMUM_READ_FIELDS = ["id"]
            self.MINIMUM_WRITE_FIELDS = ["checkout_id", "provider", "amount_paid"]
            self.SERVICE_DOMAIN_FIELDS = [
                "checkout_id",
                "provider",
                "amount_paid",
                "pk",
                "transaction_id",
                "is_successful",
            ]
            self.VALID_FIELDS_PER_ACTION = {
                "add_payment": ["checkout_id", "provider", "amount_paid"],
                "update_transaction": ["pk", "transaction_id", "is_successful"],
            }

            self.set_db_methods_fields("read_entry", "id")
            self.set_db_methods_fields("delete_entry", "id")
            self.set_db_methods_fields(
                "create_entry", "checkout_id", "provider", "amount_paid"
            )

            self.regester_method("add_payment", self.add_payment)
            self.regester_method("update_transaction", self.update_transaction)

        def add_payment(self):
            checkout_id, provider, amount_paid = self.get_method_args("add_payment")
            payment = self.parent_service.access_db_objects.create(
                checkout_id=checkout_id, provider=provider, amount_paid=amount_paid
            )
            self.behavior.service_data.update({"payment_method": payment})

        def update_transaction(self):
            payment_id, transaction_id, is_successful = self.get_method_args(
                "update_transaction"
            )
            payment = self.parent_service.db_record

            if payment:
                payment.transaction_id = transaction_id
                payment.is_successful = is_successful
                payment.save()
                self.behavior.service_data.update({"payment_method": payment})


@register_service()
class OrderSummaryModelService(BaseModelService):
    model_dependency = CheckoutAppDependency()
    model_slug = "order_summary"

    def __init__(self, session_key, *args, **db_fields):
        super().__init__(
            session_key=session_key, *args, include_session=False, **db_fields
        )
        self.validator = self.OrderSummaryValidator
        self.init_state_hook()

    class OrderSummaryValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.MINIMUM_READ_FIELDS = ["checkout_id"]
            self.MINIMUM_WRITE_FIELDS = ["checkout_id", "subtotal", "shipping_cost"]
            self.SERVICE_DOMAIN_FIELDS = [
                "checkout_id",
                "subtotal",
                "shipping_cost",
                "notes",
            ]
            self.VALID_FIELDS_PER_ACTION = {
                "create_summary": ["checkout_id", "subtotal", "shipping_cost", "notes"],
            }

            self.set_db_methods_fields("read_entry", "checkout_id")
            self.set_db_methods_fields(
                "create_entry", "checkout_id", "subtotal", "shipping_cost"
            )
            self.regester_method("create_summary", self.create_summary)

        def create_summary(self):
            checkout_id, subtotal, shipping_cost, notes = self.get_method_args(
                "create_summary"
            )
            summary = self.parent_service.access_db_objects.create(
                checkout_id=checkout_id,
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                notes=notes,
            )
            self.behavior.service_data.update({"order_summary": summary})
