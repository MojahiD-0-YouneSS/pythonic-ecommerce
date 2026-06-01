from django.views import View
from django.http import JsonResponse
from apps.cms.systems.management import CmsManagementSystem


def execute_cms_flow(request, service, method, **kwargs):
    """Helper to inject targets, run the CmsManagementSystem, and format the response."""
    rpom = request.framework_entry.request_path_object_mapper
    rpom.extra["target_service"] = service
    rpom.extra["target_method"] = method

    if kwargs:
        request.framework_entry.service_entry_data.raw_data.update(kwargs)

    system = CmsManagementSystem(request=request)
    success, entry = system.execute()

    if success:
        return JsonResponse(
            {"status": "success", "data": entry.service_entry_data.state}
        )
    return JsonResponse(
        {"status": "error", "errors": entry.service_entry_data.errors}, status=400
    )


class BaseCmsView(View):
    """
    Explicit base view for CMS models.
    Subclasses only need to define the service_slug.
    """

    service_slug = None

    def get(self, request, *args, **kwargs):
        return execute_cms_flow(request, self.service_slug, "read_entry", **kwargs)

    def post(self, request, *args, **kwargs):
        return execute_cms_flow(request, self.service_slug, "create_entry", **kwargs)

    def put(self, request, *args, **kwargs):
        return execute_cms_flow(request, self.service_slug, "update_entry", **kwargs)


# --- EXPLICIT CMS MODEL VIEWS ---


class QuoteView(BaseCmsView):
    service_slug = "quote_model_service"


class SystemBannerRotationView(BaseCmsView):
    service_slug = "system_banner_rotation_model_service"


class HomepageEditorView(BaseCmsView):
    service_slug = "homepage_editor_model_service"


class BannerView(BaseCmsView):
    service_slug = "banner_model_service"


class PosterView(BaseCmsView):
    service_slug = "poster_model_service"


class TestimonyView(BaseCmsView):
    service_slug = "testimony_model_service"


class AboutUsView(BaseCmsView):
    service_slug = "about_us_model_service"


class ContactView(BaseCmsView):
    service_slug = "contact_model_service"


class ContactUsView(BaseCmsView):
    service_slug = "contact_us_model_service"


class PageVisitView(BaseCmsView):
    service_slug = "page_visit_model_service"


class DashboardMetricsView(BaseCmsView):
    service_slug = "dashboard_metrics_model_service"
