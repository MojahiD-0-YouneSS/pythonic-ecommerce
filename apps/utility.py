from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy


class CustomAdminRequiredMixin(AccessMixin):
    """
    Grants access ONLY to Superusers OR users in the 'Store Managers' group.
    Since Store Managers do not have is_staff=True, they are completely blocked
    from accessing the native Django /admin/ panel!
    """

    login_url = reverse_lazy("client:login")

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # 1. Kick out people who aren't logged in at all
        if not user.is_authenticated:
            return self.handle_no_permission()

        # 2. Check if they belong to the special custom admin group
        is_store_manager = user.groups.filter(
            name="store_manager"
        ).exists()

        # 3. If they are neither a superuser NOR a store manager, kick them out!
        if not (user.is_superuser or is_store_manager):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        url = self.get_login_url()
        if self.request.headers.get("HX-Request") == "true":
            response = HttpResponse(status=200)
            response["HX-Redirect"] = url
            return response
        return HttpResponseRedirect(url)
