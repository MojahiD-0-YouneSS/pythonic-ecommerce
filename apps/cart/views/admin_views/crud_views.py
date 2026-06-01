from django.views import View
from django_abstract.utilities import (
    ClassInfoProvider,
    AdminOrStaffMixin,
    HtmxLoginRequiredMixin,
)
from django.http import HttpResponse
from ...forms.admin_forms.model_form import (
    DiscountCodeForm,
    CartForm,
    CartItemForm,)
from apps.global_context import get_global_context
from ui.pages.cart.admin.discount_code import admin_discout_page
from probo.request import RequestDataTransformer, FormHandler
from apps.cart.forms.admin_forms.model_form import (
    DiscountCodeForm,
)
from django.contrib import messages
from ui.components.messaging import get_messages
from probo.components import frag
from apps.utility import CustomAdminRequiredMixin

class AdminCartView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.view_info_data = ClassInfoProvider().resolve_class_info(self)

    def request_check(self, request_data):
        flag = request_data.get('guest_mode_flag')
        response = request_data.get('guest_mode_responses', None).get('htpp', None)
        if flag:
            return response
        else:
            return response

    def get(self, request, *args, **kwargs):
        request_data = RequestDataTransformer(request)
        return  self.request_check(self, request_data)

    def post(self, request, *args, **kwargs):
        # Process POST request and return response
        # not exactlly but it's good as example
        
        request_data = RequestDataTransformer(request, DiscountCodeForm)
        if request_data.is_valid():
            hundler = FormHandler()
            hundler.hundle_form(request_data)
        return  self.request_check(self, request_data)

    def put(self, request, *args, **kwargs):
        # Process PUT request and return response
        request_data = RequestDataTransformer(request)
        return  self.request_check(self, request_data)

    def delete(self, request, *args, **kwargs):
        # Process DELETE request and return response
        request_data = RequestDataTransformer(request)
        return  self.request_check(self, request_data)

    def patch(self, request, *args, **kwargs):
        # Process PATCH request and return response
        request_data = RequestDataTransformer(request)
        return  self.request_check(self, request_data)

    def __str__(self):
        return f"ActionXView(app={self.app}, action={self.action}, args={self.args})"


class AddDiscountCodeView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    _ctx = get_global_context()
    def get(self,request):
        rdt = RequestDataTransformer(request=request,form_class=DiscountCodeForm)
        with self._ctx as ctx:
            ctx.put('csrf_token', rdt.get_csrf_token())
            form = admin_discout_page(rdt=rdt)
            return HttpResponse(form.render())

    def post(self,request):
        rdt = RequestDataTransformer(request=request,form_class=DiscountCodeForm)
        if rdt.is_valid():
            rdt.save_form()
            messages.success(
                request=request, message="Discount Code is created and saved successfully"
            )
        else:
            messages.error(
                request=request, message="Discount Code is created and saved successfully"
            )
        message = get_messages(messages=messages.get_messages(request=request),hx_oob=True)
        new_form = admin_discout_page(rdt=rdt).html_doc.find(lambda n:n.attr_manager.get_attr('Id') == 'admin-form-container')

        return HttpResponse(frag(
            message,
            new_form
        ))
