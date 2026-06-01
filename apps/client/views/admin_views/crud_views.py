from django.http import HttpResponse
from django.views import View
from django_abstract.utilities import (
    ClassInfoProvider,
    AdminOrStaffMixin,
    HtmxLoginRequiredMixin,
)
from apps.global_context import get_global_context
from apps.client.dependencies import get_client_dependency
from apps.utility import CustomAdminRequiredMixin
from ui.pages.client.admin.client_report import AdminUserDetailPage

class AdminClientView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.view_info_data = ClassInfoProvider().resolve_class_info(self)

    def request_response(self, request_data):
        flag = request_data.get('guest_mode_flag')
        response = request_data.get('guest_mode_responses', None).get('http', None)
        if flag:
            return response
        else:
            return response

    def get(self, request, *args, **kwargs):
        return  self.request_response(self, request)

    def put(self, request, *args, **kwargs):
        # Process PUT request and return response
        return  self.request_response(self, request)

    def delete(self, request, *args, **kwargs):
        # Process DELETE request and return response
        return  self.request_response(self, request)

    def patch(self, request, *args, **kwargs):
        # Process PATCH request and return response
        return  self.request_response(self, request)

    def __str__(self):
       return f"ClientView(app={self.app}, action={self.action}, args={self.args})"

class GuestIdentityView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.view_info_data = ClassInfoProvider().resolve_class_info(self)

    def request_response(self, request_data):
        flag = request_data.get('guest_mode_flag')
        response = request_data.get('guest_mode_responses', None).get('http', None)
        if flag:
            return response
        else:
            return response

    def get(self, request, *args, **kwargs):
        return  self.request_response(request)

    def put(self, request, *args, **kwargs):
        # Process PUT request and return response
        return  self.request_response(self, request)

    def delete(self, request, *args, **kwargs):
        # Process DELETE request and return response
        return  self.request_response(self, request)

    def patch(self, request, *args, **kwargs):
        # Process PATCH request and return response
        return  self.request_response(self, request)

    def __str__(self):
       return f"GuestIdentityView(app={self.app}, action={self.action}, args={self.args})"

class ClientDetailView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()
    def get(self, request,user_id, *args, **kwargs):
        with self.__ctx as ctx:
            client = (
                get_client_dependency().select_client.get_by(id=user_id)
                if request.user.is_authenticated
                else None
            )
            ctx.put('client', client)
            page = AdminUserDetailPage()
            return HttpResponse(page.render())

    def post(self, request, *args, **kwargs):
        # Process PUT request and return response
        return  self.request_response(self, request)

    def __str__(self):
        return f"ClientCRUDView(app={self.app}, action={self.action}, args={self.args})"
