from apps.product.services.model_service import (
    ProductModelService,
    DynamicPricingModelService,
)
from apps.product.services.product_service import PricingEngineService


class ClientCatalogOrchestrator:
    """Aggregates catalog data and calculates live dynamic pricing for the storefront."""

    def __init__(self, session_key=None):
        self.session_key = session_key

    def get_storefront_context(self):
        # 1. Fetch Featured Products
        product_svc = ProductModelService(session_key=self.session_key)
        product_svc.entry.service_data.update({"method_name": "get_catalog"})
        product_svc.hook()
        products = product_svc.entry.service_data.get("products", [])

        formatted_products = []

        for p in products:
            primary_variant = p.variants.first()
            if not primary_variant:
                continue

            # 2. Check for Dynamic Pricing Rules
            pricing_db_svc = DynamicPricingModelService(session_key=self.session_key)
            pricing_db_svc.entry.service_data.update(
                {"method_name": "get_active_rules", "variant_id": primary_variant.id}
            )
            pricing_db_svc.hook()
            rules = pricing_db_svc.entry.service_data.get("pricing_rules", [])

            # 3. Calculate Live Price via Pure Logic Engine (Assuming quantity 1 for catalog)
            pricing_logic = PricingEngineService()
            pricing_logic.entry.service_data.update(
                {
                    "method_name": "calculate_best_price",
                    "base_price": primary_variant.base_price,
                    "quantity": 1,
                    "rules": rules,
                }
            )
            pricing_logic.hook()
            pricing_data = pricing_logic.entry.service_data

            formatted_products.append(
                {
                    "id": primary_variant.id,
                    "slug": p.slug,
                    "name": p.name,
                    "brand": p.brand.name if p.brand else None,
                    "original_price": str(pricing_data["original_price"]),
                    "price": str(pricing_data["final_price"]),
                    "has_discount": pricing_data["is_discounted"],
                    "image": (
                        primary_variant.media.first().file.url
                        if primary_variant.media.exists()
                        else "https://placehold.co/400"
                    ),
                }
            )

        return {"products": formatted_products}
