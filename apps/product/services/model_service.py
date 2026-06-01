from django_abstract.base.base_model_service import BaseModelService
from apps.product.dependencies import ProductAppDependecy
from django.utils import timezone


class ProductModelService(BaseModelService):
    model_dependency = ProductAppDependecy()
    model_slug = "product"

    def __init__(self, session_key=None, *args, **db_fields):
        super().__init__(
            session_key=session_key, *args, include_session=False, **db_fields
        )
        self.init_state_hook()

    class ProductValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.MINIMUM_READ_FIELDS = ["id"]
            self.MINIMUM_WRITE_FIELDS = ["name", "slug", "sku"]
            self.VALID_FIELDS_PER_ACTION = {
                "get_catalog": [],
                "get_product_detail": ["slug"],
            }
            self.proxy_register()

        def proxy_register(self):
            self.regester_method("get_catalog", self.get_catalog)
            self.regester_method("get_product_detail", self.get_product_detail)

        def get_catalog(self):
            # Highly optimized query fetching all the enterprise relationships!
            products = self.parent_service.access_db_objects.prefetch_related(
                "variants__color", "variants__size", "categories", "brand"
            ).filter(is_featured=True)
            self.behavior.service_data.update({"products": products})

        def get_product_detail(self):
            slug = self.get_method_args("get_product_detail")[0]
            product = (
                self.parent_service.access_db_objects.prefetch_related(
                    "variants__media", "variants__pricing_rules", "reviews", "seo"
                )
                .filter(slug=slug)
                .first()
            )
            self.behavior.service_data.update({"product": product})


class ProductVariantModelService(BaseModelService):
    model_dependency = ProductAppDependecy()
    model_slug = "product_variant"

    def __init__(self, session_key=None, *args, **db_fields):
        super().__init__(
            session_key=session_key, *args, include_session=False, **db_fields
        )
        self.validator = self.VariantValidator
        self.init_state_hook()

    class VariantValidator(BaseModelService.BaseServiceValidator):

        def meta_hook(self):
            self.MINIMUM_READ_FIELDS = ["id"]
            self.MINIMUM_WRITE_FIELDS = ["product_id", "sku", "base_price"]
            self.SERVICE_DOMAIN_FIELDS =['id','quantity']
            self.VALID_FIELDS_PER_ACTION = {
                "deduct_stock": ["id", "quantity"],
            }
            self.set_db_methods_fields("read_entry", "id")

            self.regester_method("deduct_stock", self.deduct_stock)

        def deduct_stock(self):
            variant_id, quantity = self.get_method_args("deduct_stock")
            variant = self.parent_service.db_record

            if variant and variant.stock >= quantity:
                variant.stock -= quantity
                variant.save()
                self.behavior.service_data.update({"variant": variant, "success": True})
            else:
                self.parent_service.entry.errors["stock"] = "Insufficient stock."
                self.behavior.service_data.update({"success": False})
        

class DynamicPricingModelService(BaseModelService):
    model_dependency = ProductAppDependecy()
    model_slug = "dynamic_pricing_rule"

    def __init__(self, session_key=None, *args, **db_fields):
        super().__init__(
            session_key=session_key, *args, include_session=False, **db_fields
        )
        self.init_state_hook()

    class PricingRuleValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.VALID_FIELDS_PER_ACTION = {"get_active_rules": ["variant_id"]}
            self.proxy_register()

        def proxy_register(self):
            self.regester_method("get_active_rules", self.get_active_rules)

        def get_active_rules(self):
            variant_id = self.get_method_args("get_active_rules")[0]
            now = timezone.now()
            # Fetch rules currently valid by date
            rules = self.parent_service.access_db_objects.filter(
                variant_id=variant_id, start_date__lte=now, end_date__gte=now
            )
            self.behavior.service_data.update({"pricing_rules": rules})
