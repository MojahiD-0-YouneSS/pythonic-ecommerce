from django.http import HttpResponse
from django.views import View
from django_abstract.utilities import (
    ClassInfoProvider,
    AdminOrStaffMixin,
    HtmxLoginRequiredMixin,
)
from probo.components import frag, Frag
from apps.global_context import get_global_context
from apps.order.dependencies import get_order_dependency
from apps.utility import CustomAdminRequiredMixin
from ui.pages.order.admin.order_management import OrderManagementPage


class OrderManagementView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self, request, order_id, *args, **kwargs):
        # Ensure dependencies are loaded
        order = get_order_dependency().select_order.get_by(id=order_id)
        # Get global context (which should include orders)
        with request.ui_context as ctx:
            ctx.put('order', order)
            # Render the Order Management Page with the orders
            page = OrderManagementPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))
