from django_abstract.base.base_model_service import BaseModelService 
from apps.order.dependencies import OrderAppDependency
from django_abstract.registry import register_service

@register_service()
class OrderModelService(BaseModelService):
    model_dependency = OrderAppDependency()
    model_slug = "order"
    hooks_list = ['order_item_model_service',]

    def __init__(self, session_key,*args,include_session=True,auto_create=False,**db_fields):
        super().__init__(
            session_key=session_key,
            *args,
            include_session=include_session,
            auto_create=auto_create,
            **db_fields
        )
        self.validator = self.OrderValidator
        self.init_state_hook()

    class OrderValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            # NOTE: If tracking_number is blank on creation, requiring it for READ might block
            # you from fetching new orders! Consider changing it to just 'session_key' or 'id'.
            self.MINIMUM_READ_FIELDS = ["session_key", "tracking_number"]
            self.MINIMUM_WRITE_FIELDS = [
                "session_key",
                "total_amount",
                "tracking_number",
            ]
            self.SERVICE_DOMAIN_FIELDS = [
                "tracking_number",
                "session_key",
                "address_id",
                "address_type",
                "total_amount",
                "status",
                "new_tracking_number",
            ]

            # 1. Action Registries
            self.VALID_FIELDS_PER_ACTION = {
                "update_addresses": [
                    "tracking_number",
                    "session_key",
                    "address_id",
                    "address_type",
                ],
                "mark_payment_status": ["session_key", "tracking_number", "status"],
                "mark_order_status": ["session_key", "tracking_number", "status"],
                "set_tracking": [
                    "session_key",
                    "tracking_number",
                    "new_tracking_number",
                ],
                "cancel_order": ["session_key", "tracking_number"],
                "refund_order": ["session_key", "tracking_number"],
            }

            self.set_db_methods_fields("read_entry", "session_key")
            self.set_db_methods_fields("delete_entry", "session_key")
            self.set_db_methods_fields("create_entry", "session_key", "total_amount")

            self.regester_method(
                "update_addresses", self.update_address
            )  # Mapped to singular method name
            self.regester_method("mark_payment_status", self.mark_payment_status)
            self.regester_method("mark_order_status", self.mark_order_status)
            self.regester_method("set_tracking", self.set_tracking)
            self.regester_method("cancel_order", self.cancel_order)
            self.regester_method("refund_order", self.refund_order)

        def update_address(self):
            tracking_number, session_key, address_id, address_type = (
                self.get_method_args("update_addresses")
            )

            # OPTIMIZATION: Use the already-fetched order! No extra DB hit!
            order = self.parent_service.db_record

            if not order:
                return

            if address_type == "billing":
                billing_address = self.dependency.select_billing_address.get_by(
                    id=address_id
                )
                if billing_address:
                    order.billing_address = billing_address

            elif address_type == "shipping":
                shipping_address = self.dependency.select_shipping_address.get_by(
                    id=address_id
                )
                if shipping_address:
                    order.shipping_address = shipping_address

            order.save()
            # Better to pass the object or dict safely rather than __dict__ to avoid _state issues
            self.behavior.service_data.update({"order": order})

        def mark_payment_status(self):
            session_key, tracking_number, status = self.get_method_args(
                "mark_payment_status"
            )
            order = self.parent_service.db_record

            if order:
                order.payment_status = status
                order.save()
                self.behavior.service_data.update({"order": order})

        def mark_order_status(self):
            session_key, tracking_number, status = self.get_method_args(
                "mark_order_status"
            )
            order = self.parent_service.db_record

            if order:
                order.status = status
                order.save()
                self.behavior.service_data.update({"order": order})

        def set_tracking(self):
            session_key, tracking_number, new_tracking_number = self.get_method_args(
                "set_tracking"
            )
            order = self.parent_service.db_record

            if order:
                order.tracking_number = new_tracking_number
                order.status = "Shipped"  # Auto-update status when tracking is added
                order.save()
                self.behavior.service_data.update({"order": order})

        def cancel_order(self):
            session_key, tracking_number = self.get_method_args("cancel_order")
            order = self.parent_service.db_record

            if order and order.status not in ["Shipped", "Delivered"]:
                order.status = "Canceled"
                order.save()
                self.behavior.service_data.update(
                    {"order": order, "message": "Order canceled successfully."}
                )

        def refund_order(self):
            session_key, tracking_number = self.get_method_args("refund_order")
            order = self.parent_service.db_record

            if order:
                order.payment_status = "Refunded"
                order.status = "Returned"
                order.save()
                self.behavior.service_data.update(
                    {"order": order, "message": "Order refunded successfully."}
                )


@register_service()
class OrderItemModelService(BaseModelService):
    model_dependency = OrderAppDependency()
    model_slug = "order_item"
    hooks_list =['order_model_service']

    def __init__(self, session_key,*args,include_session=True, load_record=False,**db_fields):
        super().__init__(session_key=session_key,*args,include_session=include_session,load_record=load_record)
        self.validator = self.OrderItemValidator
        self.init_state_hook()

    class OrderItemValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            # 'id' is used to target a specific order item for updates/reads
            self.MINIMUM_READ_FIELDS = ["order_id"]
            self.MINIMUM_WRITE_FIELDS = [
                "order_id",
                "product_variant_id",
                "quantity",
                "price",
            ]
            self.SERVICE_DOMAIN_FIELDS = [
                "order_id",
                "product_variant_id",
                "quantity",
                "price",
                "pk",
            ]

            # 1. Action Registries
            self.VALID_FIELDS_PER_ACTION = {
                "add_order_item": [
                    "order_id",
                    "product_variant_id",
                    "quantity",
                    "price",
                ],
                "update_item_quantity": ["pk", "quantity"],
                "remove_order_item": ["pk"],
                "get_order_items": ["order_id"],
            }

            # 2. Map CRUD reserved actions
            self.set_db_methods_fields("read_entry", "order")
            self.set_db_methods_fields("delete_entry", "pk")
            self.set_db_methods_fields(
                "create_entry", "order", "product_variant", "quantity", "price"
            )

            # Note: Using your framework's spelling of 'regester_method'
            self.regester_method("add_order_item", self.add_order_item)
            self.regester_method("update_item_quantity", self.update_item_quantity)
            self.regester_method("remove_order_item", self.remove_order_item)
            self.regester_method("get_order_items", self.get_order_items)

        # --- 3. Implement the Business Logic ---

        def add_order_item(self):
            order_id, product_variant_id, quantity, price = self.get_method_args(
                "add_order_item"
            )

            # OPTIMIZATION: Using _id fields directly skips querying the parent instances!
            # It maps directly to Django's foreign key backend logic.
            order_item = self.parent_service.access_db_objects.create(
                order_id=order_id,
                product_variant_id=product_variant_id,
                quantity=quantity,
                price=price,
            )
            self.behavior.service_data.update({"order_item": order_item})

        def update_item_quantity(self):
            item_id, quantity = self.get_method_args("update_item_quantity")

            # Use the record fetched by the BaseOperatorService init_state_hook
            order_item = self.parent_service.db_record

            if order_item:
                order_item.quantity = quantity
                order_item.save()
                self.behavior.service_data.update({"order_item": order_item})

        def remove_order_item(self):
            item_id = self.get_method_args("remove_order_item")[0]

            order_item = self.parent_service.db_record

            if order_item:
                order_item.delete()
                self.behavior.service_data.update(
                    {"message": "Order item successfully removed."}
                )

        def get_order_items(self):
            order_id = self.get_method_args("get_order_items")[0]

            # Fetch all items belonging to the specific order
            items = self.parent_service.access_db_objects.filter(order_id=order_id)

            self.behavior.service_data.update({"order_items": items})

# class BillingAddressModelService(BaseModelService):
#     model_dependency = OrderAppDependency()
#     model_slug = "billing_address"

#     def __init__(self, session_key,*args,include_session=True, include_session_key_as=None,**db_fields):
#         super().__init__(session_key=session_key,*args,include_session=include_session,include_session_key_as=include_session_key_as)
#         self.init_state_hook()

#     class BillingAddressValidator(BaseModelService.BaseServiceValidator):
#         def meta_hook(self):
#             self.MINIMUM_READ_FIELDS = []
#             self.MINIMUM_WRITE_FIELDS = []
#             self.VALID_FIELDS_PER_ACTION = {}


# class ShippingAddressModelService(BaseModelService):
#     model_dependency = OrderAppDependency()
#     model_slug = "shipping_address"

#     def __init__(self, session_key,*args,include_session=True, include_session_key_as=None,**db_fields):
#         super().__init__(session_key=session_key,*args,include_session=include_session,include_session_key_as=include_session_key_as)
#         self.init_state_hook()

#     class ShippingAddressValidator(BaseModelService.BaseServiceValidator):
#         def meta_hook(self):
#             self.MINIMUM_READ_FIELDS = []
#             self.MINIMUM_WRITE_FIELDS = []
#             self.VALID_FIELDS_PER_ACTION = {}


# class OrderVerificationModelService(BaseModelService):
#     model_dependency = OrderAppDependency()
#     model_slug = "order_verification"

#     def __init__(self, session_key,*args,include_session=True, include_session_key_as=None,**db_fields):
#         super().__init__(session_key=session_key,*args,include_session=include_session,include_session_key_as=include_session_key_as)
#         self.init_state_hook()

#     class OrderVerificationValidator(BaseModelService.BaseServiceValidator):
#         def meta_hook(self):
#             self.MINIMUM_READ_FIELDS = []
#             self.MINIMUM_WRITE_FIELDS = []
#             self.VALID_FIELDS_PER_ACTION = {}
