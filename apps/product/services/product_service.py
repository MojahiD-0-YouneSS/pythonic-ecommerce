from django_abstract.base.base_service import BaseService
from decimal import Decimal


class PricingEngineService(BaseService):
    """
    Pure Business Logic: Calculates dynamic discounts based on complex enterprise rules.
    Does NOT touch the database.
    """

    hooks_list = []

    def __init__(self, session_key=None, **raw_data):
        self.validator = self.PricingEngineValidator
        super().__init__(session_key=session_key, **raw_data)

    class PricingEngineValidator(BaseService.BaseServiceValidator):
        def meta_hook(self):
            self.VALID_FIELDS_PER_ACTION = {
                "calculate_best_price": ["base_price", "quantity", "rules"]
            }
            self.proxy_register()

        def proxy_register(self):
            self.regester_method("calculate_best_price", self.calculate_best_price)

        def calculate_best_price(self):
            base_price, quantity, rules = self.get_method_args("calculate_best_price")
            base_price = Decimal(str(base_price))

            best_discount_pct = Decimal("0.00")

            # Evaluate all active rules to find the highest applicable discount
            if rules:
                for rule in rules:
                    if rule.min_quantity <= quantity <= rule.max_quantity:
                        discount = Decimal(str(rule.discount_percentage))
                        if discount > best_discount_pct:
                            best_discount_pct = discount

            discount_amount = base_price * (best_discount_pct / Decimal("100"))
            final_price = (base_price - discount_amount).quantize(Decimal("0.01"))

            self.behavior.service_data.update(
                {
                    "original_price": base_price,
                    "final_price": final_price,
                    "applied_discount_pct": best_discount_pct,
                    "is_discounted": best_discount_pct > 0,
                }
            )
