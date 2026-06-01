from django_abstract.base.base_system import BaseSystem


class CmsManagementSystem(BaseSystem):
    """
    Orchestrates complex content management workflows.
    Used primarily by the Admin Dashboard endpoints.
    """

    allowed_operators = ["cms_operator"]

    def __init__(self, entry=None, request=None):
        # Supports being initialized by the Unified View (entry)
        # or the Legacy Middleware (request)
        if request and not entry:
            entry = getattr(request, "framework_entry", None)

        super().__init__(entry=entry)

    def execute(self):
        if not self.entry:
            return False, "Critical: Framework Entry missing."

        rpom = self.entry.request_path_object_mapper

        # Safely extract target from URL mapper
        if len(rpom.list_url) >= 3:
            target_service = f"{rpom.list_url[1]}_model_service"
            target_method = rpom.list_url[2]
        else:
            self.entry.service_entry_data.errors["routing"] = "Invalid CMS API path."
            return False, self.entry

        # Delegate security to the CMS Operator
        success = self.invoke_operator(
            operator_name="cms_operator",
            target_service=target_service,
            target_method=target_method,
        )

        # Example System-level Logic: Triggering analytics update asynchronously
        if success and target_service == "page_visit_model_service":
            self.trigger_dashboard_metrics_compilation()

        return success, self.entry

    def trigger_dashboard_metrics_compilation(self):
        """
        Placeholder for a background task (e.g., Celery)
        to re-calculate the DashboardMetrics model.
        """
        pass
