from django.http import HttpResponse
from django.views import View
from apps.order.dependencies import get_order_dependency
from ui.components.order.admin.order_management import OrderManagementSection
from apps.utility import CustomAdminRequiredMixin
from probo.components import frag,Frag
from django_abstract.utilities import HtmxLoginRequiredMixin


class OrderProssingView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        # Ensure dependencies are loaded
        order = get_order_dependency().select_order.get_by(id=order_id)
        # Get global context (which should include orders)
        payment_status, order_status, tracking_number = (
            request.POST.get('payment_status'),
            request.POST.get('status'),
            request.POST.get('tracking_number'),
            
            )
        if not order.tracking_number:
            order.tracking_number = tracking_number
        order.status = order_status
        order.payment_status = payment_status
        order.save()
        # order_svc = OrderModelService(session_key=request.session.session_key,load_record=False)

        with request.ui_context as ctx:
            ctx.put('order', order)
            # Render the Order Management Page with the orders                 Id="order-processing-form",
            ctx.put('hx_oob', 'true')
            page = OrderManagementSection().find(lambda n:n.attr_manager.get_id() == "order-processing-form")
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))
