from django.views import View
from django_abstract.utilities import (
    ClassInfoProvider,
)

class ClientProfileView(View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.view_info_data = ClassInfoProvider().resolve_class_info(self)

    def request_response(self, request_data):
        flag = request_data.get('guest_mode_flag')
        response = request_data.get('guest_mode_responses', None).get('htpp', None)
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
       return f"ClientProfileView(app={self.app}, action={self.action}, args={self.args})"

class ShoppingHistoryView(View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.view_info_data = ClassInfoProvider().resolve_class_info(self)

    def request_response(self, request_data):
        flag = request_data.get('guest_mode_flag')
        response = request_data.get('guest_mode_responses', None).get('htpp', None)
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
       return f"ShoppingHistoryView(app={self.app}, action={self.action}, args={self.args})"
