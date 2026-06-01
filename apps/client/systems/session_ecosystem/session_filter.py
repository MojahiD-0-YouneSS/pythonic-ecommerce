from django_abstract.base.base_system import BaseSystem
from django_abstract.utilities import ExtractRequestDataUtilities, to_snake_case
from django_abstract.registry import register_system

@register_system()
class SessionFilterSystem(BaseSystem):
    """
    The main entry point for all frontend user traffic.
    Extracts HTTP data, builds the Entry envelope, and delegates to the ClientOperator.
    """

    # This system strictly uses the client_operator to enforce boundaries
    ALLOWED_OPERATORS = ["session_operator"]
    SYSTEM_SLUG  = "session_filter_system"
    def __init__(self, request):
        # BaseSystem handles the initial entry/session creation
        super().__init__(request=request)

    def execute(self):
        # 1. Extract context and fully hydrate the Entry & RPOM using your new utility
        extractor = ExtractRequestDataUtilities(self.request)
        self.entry = extractor.populate_entry(self.entry)

        # 2. Extract routing targets dynamically from the populated RPOM
        rpom = self.entry.request_path_object_mapper

        # Example: if path is /api/cart/add_item/
        # app = "cart", list_url = ["api", "cart", "add_item"]
        if len(rpom.list_url) >= 3:
            target_service = (
                f"{rpom.list_url[1]}_model_service"  # e.g., "cart_model_service"
            )
            target_method = rpom.list_url[2]  # e.g., "add_item"
        else:
            self.entry.service_entry_data.errors["routing"] = (
                "Invalid API path structure."
            )
            return False, self.entry

        # 3. Pass the fully hydrated Entry to the Operator
        success = (
            self.invoke_operator(
            operator_name="session_operator",
            target_service=target_service,
            target_method=target_method,
        )
            )

        return success, self.entry
