from apps.cart.dependencies import CartAppDependency
from django_abstract.utilities import EntryValidator, ServiceEntryData
from django_abstract.base.base_model_service import BaseModelService
from apps.product.dependencies import get_product_app_dependency
from decimal import Decimal
from django_abstract.registry import register_service
from django.forms.models import model_to_dict

@register_service()
class CartModelService(BaseModelService):
    model_dependency = CartAppDependency()
    model_slug = "cart"
    hooks_list = ['cart_item_model_service',]
    service_slug = 'cart_model_service'

    def __init__(self, session_key, *args,load_record=True, **db_required_fields):
        super().__init__(
            session_key=session_key,
            *args,
            include_session=True,
            auto_create=True,
            load_record=load_record,
            include_session_key_as="session",
            **db_required_fields
        )
        self.validator = self.CartServiceValidator
        self.init_state_hook()
        if 'session' not in self.entry.service_data and 'session' in self.entry.raw_data:
            self.entry.service_data["session"] = self.entry.raw_data["session"]

    class CartServiceValidator(BaseModelService.BaseServiceValidator):

        def meta_hook(self):
            # Run at initialization to set up rules securely
            self.MINIMUM_WRITE_FIELDS = ["session",]
            self.MINIMUM_READ_FIELDS = ["session",]
            self.SERVICE_DOMAIN_FIELDS = ["session",]
            self.VALID_FIELDS = {}
            self.VALID_FIELDS_PER_ACTION = {
                "clear_cart": ["session"],
                "get_cart": ["session"],
            }
            self.RESERVED_DB_METHODS = {
                "read_entry": ["session"],
                "delete_entry": ["session"],
                "create_entry": ["session"],
            }

            self.regester_method("get_cart", self.get_cart)
            self.regester_method("clear_cart", self.clear_cart)

        def get_cart(self,*args,**kwargs):

            # Extract safely, get_method_args returns a list
            session = self.get_method_args("get_cart")[0]
            cart = self.dependency.select_cart.get_by(session=session)
            cart_items = self.dependency.select_cart_item.filter_by(
                is_active=True, cart=cart
            )
            sub_total_list = [item.product_variant.base_price * item.quantity for item in cart_items]
            cart_total = sum(item.product_variant.base_price * item.quantity for item in cart_items)
            self.behavior.service_data.update(
                {
                    "cart": (cart),
                    "cart_items": [(item) for item in cart_items],
                    "sub_total_list": sub_total_list,
                    "cart_total": cart_total,
                    "total_items": len(cart_items),
                    "total_quantity": sum(item.quantity for item in cart_items),
                }
            )

        def clear_cart(self):
            session = self.get_method_args("clear_cart")[0]
            # Because get_cart_items sets self.behavior.service_data, we fetch from there
            items = self.behavior.service_data.get("cart_items", [])
            if not items:
                items = self.dependency.select_cart.get_by(session=session).items.filter(is_active=True)
            self.is_cross_domain = True
            sed = ServiceEntryData()
            sed.service_data["service_args"] = (
                {
                     'session_key':session,
                     'load_record':False,
                }
            )
            sed.service_data["method_name"] = (
                "remove_item_from_cart"
            )

            for item in items:
                self.cross_domain_data.update({"pk": item.id, "session": session})
                sed.service_data.update(self.cross_domain_data)
                if self.parent_service:
                    self.parent_service.hook_pad('cart_item_model_service',entry=sed)
            self.is_cross_domain = False
            self.get_cart()

@register_service()
class CartItemModelService(BaseModelService):
    model_dependency = CartAppDependency()
    model_slug = "cart_item"
    hooks_list = ['cart_model_service']

    def __init__(self, session_key, *args,load_record=True, **db_required_fields):
        super().__init__(
            session_key=session_key,
            *args,
            include_session=False,
            load_record=load_record,
            **db_required_fields
        )
        self.validator = self.CartItemServiceValidator
        self.init_state_hook()

    class CartItemServiceValidator(BaseModelService.BaseServiceValidator):

        def meta_hook(self):
            # Run at initialization to set up rules securely
            self.MINIMUM_WRITE_FIELDS = ["cart", "product_variant", "quantity"]
            self.MINIMUM_READ_FIELDS = ["cart", "product_variant"]
            self.SERVICE_DOMAIN_FIELDS = [
                "session",
                "pk",
                "product_variant", "quantity",
            ]
            self.VALID_FIELDS = {}

            self.VALID_FIELDS_PER_ACTION = {
                "add_item_to_cart": ["product_variant", "quantity", "session"],
                "remove_item_from_cart": [
                    "pk",
                ],
                "update_item_quantity": ["pk", "quantity", "session"],
                "get_item": ["pk",],
                "get_cart_items": ["session"],
            }

            self.set_db_methods_fields("read_entry", "cart")
            self.set_db_methods_fields("create_entry", "cart")
            self.set_db_methods_fields("delete_entry", "pk")

            self.regester_method("add_item_to_cart", self.add_item_to_cart)
            self.regester_method("remove_item_from_cart", self.remove_item_from_cart)
            self.regester_method("update_item_quantity", self.update_item_quantity)
            self.regester_method("get_cart_items", self.get_cart_items)
            self.regester_method("get_item", self.get_item)

        def add_item_to_cart(self):
            product_variant_id, quantity, session = self.get_method_args(
                "add_item_to_cart"
            )
            cart = self.dependency.select_cart.get_by(session=session)
            product_app_dependency = get_product_app_dependency()
            product = product_app_dependency.select_product_variant.get_by(
                id=product_variant_id
            )
            if product.stock == 0:
                 
                self.get_cart_items()
                self.behavior.service_data['created']=False

                return
            cart_item, _ = self.dependency.create_cart_item.access_db.get_or_create(
                product_variant=product, cart=cart
            )
            if cart_item.is_active and not cart_item.is_disabled:
                cart_item.quantity += quantity
            else:
                cart_item.is_active=True
                cart_item.is_disabled = False
                cart_item.quantity = quantity

            cart_item.save()
            product.save()
            self.get_cart_items()
            self.behavior.service_data['created']=True

        def remove_item_from_cart(self):
            pk = self.get_method_args("remove_item_from_cart")[0]
            cart_item = self.dependency.select_cart_item.access_db.get(id=pk)
            if cart_item.is_active and not cart_item.is_disabled:
                product_app_dependency = get_product_app_dependency()
                product = product_app_dependency.select_product_variant.access_db.get(
                    id=cart_item.product_variant.id
                )

                cart_item.is_active = False
                cart_item.is_disabled = True
                product.stock += cart_item.quantity
                cart_item.quantity = 0
                cart_item.save()
                product.save()
            self.get_cart_items()

        def get_cart_items(self):
            # Extract safely, get_method_args returns a list
            session = self.get_method_args("get_cart_items")[0]
            cart = self.dependency.select_cart.access_db.get(session=session)
            cart_items = self.dependency.select_cart_item.access_db.filter(
                is_active=True, cart=cart
            )
            sub_total_list = [item.product_variant.base_price * item.quantity for item in cart_items]
            cart_total = sum(item.product_variant.base_price * item.quantity for item in cart_items)

            self.behavior.service_data.update(
                {
                    "cart": (cart),
                    "cart_items": [(item) for item in cart_items],
                    "sub_total_list": sub_total_list,
                    "cart_total": cart_total,
                    "total_items": len(cart_items),
                    "total_quantity": sum(item.quantity for item in cart_items),
                }
            )

        def get_item(self):
            # Extract safely, get_method_args returns a list
            pk = self.get_method_args("get_item")[0]
            item = self.dependency.select_cart_item.access_db.get(
                id=pk
            )

            self.behavior.service_data.update(
                {
                    "item":item,
                    "cart": (item.cart),
                }
            )

        def update_item_quantity(self):
            pk, quantity,_ = self.get_method_args("update_item_quantity")
            cart_item = self.dependency.select_cart_item.get_by(id=pk)
            if cart_item.quantity == quantity and cart_item.is_active:
                self.get_cart_items()
                self.behavior.service_data["item"] = cart_item
                return 
            product_app_dependency = get_product_app_dependency()
            product = product_app_dependency.select_product_variant.get_by(
                id=cart_item.product_variant.id
            )

            if cart_item.quantity > quantity:
                diff = cart_item.quantity - quantity
                product.stock += diff
                cart_item.quantity -= diff
            else:
                diff = quantity - cart_item.quantity
                product.stock -= diff
                cart_item.quantity += diff

            cart_item.save()
            product.save()

            self.get_cart_items()
            self.behavior.service_data["item"] = cart_item

@register_service()
class DiscountCodeModelService(BaseModelService):
    model_dependency = CartAppDependency()
    model_slug = 'discount_code'

    def __init__(self, session_key, *args, auto_create=False,**db_required_fields):

        super().__init__(
            session_key=session_key,
            *args,
            auto_create=auto_create,
            include_session=False,
            **db_required_fields
        )
        self.validator = self.DiscountCodeServiceValidator
        self.init_state_hook()

    class DiscountCodeServiceValidator(BaseModelService.BaseServiceValidator):

        def meta_hook(self):

            self.MINIMUM_WRITE_FIELDS = ["code"]
            self.MINIMUM_READ_FIELDS = ["code"]
            self.SERVICE_DOMAIN_FIELDS = [ "pk", "code"]
            self.VALID_FIELDS_PER_ACTION = {
                "add_discount_code": ["code", ],
                "remove_discount_code": ["pk", ],
                "get_discount_code": ["pk", ],
                "get_discount_codes": [],
                "get_total_discount": ["code"],
                "apply_global": [],
                "get_active_codes": [],
            }

            self.regester_method("remove_discount_code", self.remove_discount_code)
            self.regester_method("get_discount_code", self.get_discount_code)
            self.regester_method("get_total_discount", self.get_total_discount)
            self.regester_method("apply_global", self.apply_global)
            self.regester_method("get_active_codes", self.get_active_codes)
            self.regester_method("get_discount_codes", self.get_discount_codes)

        def remove_discount_code(self,):

            pk = self.get_method_args("remove_discount_code")[0]
            code = self.dependency.select_discount_code.get_by(id=pk)
            code.is_active = False
            code.is_disabled = False
            code.save()
            self.behavior.service_data.update({"code": (code)})

        def get_discount_code(self,):
            pk = self.get_method_args('get_discount_code',)[0]         
            code = self.dependency.select_discount_code.get(id=pk)
            self.behavior.service_data.update({"code": (code)})

        def get_total_discount(self,):
            # Logic to get all discount codes applied to the cart
            code = self.dependency.select_discount_code.get(is_active=True, code=self.get_method_args('get_total_discount',)[0])

            self.behavior.service_data.update( {"discount_rate": code.discount_percentage,})

        def apply_global(self):
            # Logic to get all discount codes applied to the cart
            self.get_discount_codes()
            codes = self.behavior.service_data['codes']
            total = Decimal('0.00')
            self.is_cross_domain=True
            for code in codes:
                if code.is_active:
                    self.cross_domain_data.update({"code":code.code})
                    self.get_total_discount()
                    total += Decimal(self.behavior.service_data['discount_rate'])
            self.is_cross_domain=False
            self.behavior.service_data.update( { "total_discount_rate": total,})

        def get_active_codes(self,):
            codes = self.dependency.selctors.select_discount_code.filter(is_active=True)
            self.behavior.service_data.update( {'codes':[(code) for code in codes]})

        def get_discount_codes(self,):
            codes = self.dependency.select_discouint_code.all()
            self.behavior.service_data.update( {'codes':[(code) for code in codes]})
