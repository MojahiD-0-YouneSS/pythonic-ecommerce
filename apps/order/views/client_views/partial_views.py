from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse
from apps.order.dependencies import OrderAppDependency
from apps.order.forms.client_forms.model_form import BillingAddressModelForm
from ui.components.order.client_form import AddAddressForm
from ui.components.client.profile import (
    OrderHistorySection,
    AddressBookSection,
)
from django.forms.models import model_to_dict
from probo.components import frag,Frag
from ui.components.order.order_detail import OrderDetailSection

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
        with request.ui_context as ctx:
            ctx.put('orders',orders)
            ui = OrderHistorySection()
            return HttpResponse(frag(Frag(ui,data_pipeline=ctx)))

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
        with request.ui_context as ctx:
            ctx.put('addresses',addresses)
            ui = AddressBookSection()
            return HttpResponse(frag(Frag(ui,data_pipeline=ctx)))

class AddAddressView(View):
    """Handles Get, Post (Create), and Put (Update) for Client Profiles."""

    def get(self, request, *args, **kwargs):
        form = BillingAddressModelForm()

        with request.ui_context as ctx:
            ctx.put('form',form)
            ui = AddAddressForm()
            return HttpResponse(frag(Frag(ui, data_pipeline=ctx)))

    def post(self, request, *args, **kwargs):
        form = BillingAddressModelForm(request.POST)
        if form.is_valid():
            obj = form.save()
            
            obj.session_key = request.session.session_key
            obj.save()
            return redirect("order:billing-address")
        with request.ui_context as ctx:
            ctx.put('form',form)
            ui = AddAddressForm()
            return HttpResponse(frag(Frag(ui,data_pipeline=ctx)))

class OrderDetailView(View):
    """View for displaying details of a specific order."""

    def get(self, request, order_id, *args, **kwargs):
        if not request.ui_context.get('session_key'):
            request.ui_context.put('session_key', request.session.session_key)

        from apps.order.services.model_service import OrderModelService
        service = OrderModelService(request.ui_context.get("session_key"))

        order = service.entry.raw_data

        with request.ui_context as ctx:
            ctx.put('order',order)
            ui = OrderDetailSection()
            return HttpResponse(frag(Frag(ui, data_pipeline=ctx)))