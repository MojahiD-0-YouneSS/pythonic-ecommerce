from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from apps.global_context import get_global_context
from ui.pages.cart.client.cart_page import CartPage
from ui.components.cart.client.discount_code import DiscountCode
from apps.cart.models import Cart,CartItem, DiscountCode
from django_abstract.utilities import ServiceEntryData
from apps.cart.services.cart_service import CartModelService,CartItemModelService, DiscountCodeModelService


class CartView(View):
    __global_context = get_global_context()

    def get(self,request, *args, **kwargs):
        if not self.__global_context.get('session_key'):
            self.__global_context.put('session_key',request.session.session_key)
        cart_service = CartModelService(session_key=self.__global_context.get("session_key"))
        cart_service.entry.service_data["method_name"]= "get_cart"
        data = cart_service.hook()
        with self.__global_context as ctx:
            ctx.push(**cart_service.entry.service_data)
            items = CartItem.objects.filter(cart=ctx.get('cart'),is_active=True)
            ctx.put("cart_items", data.service_data.get("total_items"))
            page = CartPage(cart=ctx.get("cart"),items=items, title="Your cart Sir")
            return HttpResponse(page.render())


class DiscountCodeView(View):
    __global_context = get_global_context()

    def get(self,request, *args, **kwargs):
        if not self.__global_context.get('session_key'):
            self.__global_context.put('session_key',request.session.session_key)
        discount_service = DiscountCodeModelService(
            session_key=self.__global_context.get("session_key")
        )
        discount_entry = ServiceEntryData()
        discount_entry.service_data["method_name"] = "get_active_codes"
        discount_svc_data = discount_service.hook()
        page = DiscountCode(
            code=discount_svc_data.service_data["codes"],
        )
        return HttpResponse(page.render())
