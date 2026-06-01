from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from apps.order.dependencies import OrderAppDependency
from apps.global_context import get_global_context
from django.forms.models import model_to_dict
from apps.order.forms.client_forms.model_form import BillingAddressModelForm
from ui.components.order.client_form import AddAddressForm
from ui.components.client.profile import (
    OrderHistorySection,
    AddressBookSection,
)
from django.forms.models import model_to_dict

class OrderHistoryView(View):
    """Handles Get, Post (Create), and Put (Update) for Client Profiles."""

    def get(self, request, *args, **kwargs):
        def mapping(item):
            item_dict = model_to_dict(item)
            item_dict["id"] = str(item.id)
            return item_dict
        orders = [ mapping(item) for item in  OrderAppDependency().select_order.access_db.filter(
            session_key=request.session.session_key
        )]

        ui = OrderHistorySection(orders=orders)
        return HttpResponse(ui.render())

class AddressBookView(View):
    """Handles Get, Post (Create), and Put (Update) for Client Profiles."""

    def get(self, request, *args, **kwargs):
        def mapping(item):
            item_dict = model_to_dict(item)
            item_dict["id"] = str(item.id)
            return item_dict
        addresses = [
            mapping(item)
            for item in OrderAppDependency().select_billing_address.access_db.filter(
                session_key=request.session.session_key
            )
        ]
        ui = AddressBookSection(addresses=addresses)
        return HttpResponse(ui.render())

class AddAddressView(View):
    """Handles Get, Post (Create), and Put (Update) for Client Profiles."""

    def get(self, request, *args, **kwargs):
        form = BillingAddressModelForm()
        ui = AddAddressForm(form)
        return HttpResponse(ui.render())

    def post(self, request, *args, **kwargs):
        form = BillingAddressModelForm(request.POST)
        if form.is_valid():
            obj = form.save()
            
            obj.session_key = request.session.session_key
            obj.save()
            return redirect("order:billing-address")
        ui = AddAddressForm(form)
        return HttpResponse(ui.render())
