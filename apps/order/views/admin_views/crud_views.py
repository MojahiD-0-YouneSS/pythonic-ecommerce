from django.http import HttpResponse
from django.views import View
from django_abstract.utilities import (
    ClassInfoProvider,
    AdminOrStaffMixin,
    HtmxLoginRequiredMixin,
)
from apps import order
from apps.global_context import get_global_context
from apps.order.dependencies import get_order_dependency
from apps.utility import CustomAdminRequiredMixin
from ui.pages.order.admin.order_management import OrderManagementPage


class OrderManagementView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()
    def get(self, request, order_id, *args, **kwargs):
        # Ensure dependencies are loaded
        order = get_order_dependency().select_order.get_by(id=order_id)
        # Get global context (which should include orders)
        with self.__ctx as ctx:
            ctx.put('order', order)
            # Render the Order Management Page with the orders
            page = OrderManagementPage()
            return HttpResponse(page.render())
