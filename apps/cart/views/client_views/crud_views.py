from apps.cart.forms.client_forms.custom_form import QuantityUpdateForm
from probo.components import frag
from django.http import HttpResponse
from django.views import View
from ui.pages.cart.client.cart_page import CartPage
from ui.components.cart.client.discount_code import DiscountCode
# from apps.cart.models import Cart,CartItem, DiscountCode
from django_abstract.utilities import ServiceEntryData
from apps.cart.services.cart_service import CartModelService,CartItemModelService, DiscountCodeModelService


class CartView(View):

    def get(self,request, *args, **kwargs):
        if not request.ui_context.get('session_key'):
            request.ui_context.put('session_key',request.session.session_key)
        cart_service = CartModelService(session_key=request.ui_context.get("session_key"))
        cart_service.entry.service_data["method_name"]= "get_cart"
        data = cart_service.hook()
        with request.ui_context as ctx:
            ctx.push(**cart_service.entry.service_data)
            # items = CartItem.objects.filter(cart=ctx.get('cart'),is_active=True)
            ctx.put("total_items", data.service_data.get("total_items"))
            ctx.put("qty_form", QuantityUpdateForm())
            ctx.put('title',"Your Shopping Cart")
            page = CartPage()
            page.load_data(ctx)
            return HttpResponse(frag(page))

class DiscountCodeView(View):

    def get(self,request, *args, **kwargs):
        if not request.ui_context.get('session_key'):
            request.ui_context.put('session_key',request.session.session_key)
        try:
            discount_service = DiscountCodeModelService(
                session_key=request.ui_context.get("session_key")
            )
            discount_entry = ServiceEntryData()
            discount_entry.service_data["method_name"] = "get_active_codes"
            discount_svc_data = discount_service.hook(entry=discount_entry)
            data = discount_svc_data.service_data["codes"]
        except Exception:
            data = {'codes':[]}
        with request.ui_context as ctx:
            ctx.put('code',data["codes"])
            page = DiscountCode()
            page.load_data(ctx)
            return HttpResponse(frag(page))
