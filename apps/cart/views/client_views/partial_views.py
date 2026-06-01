from ui.components.messaging import get_messages 
from django.contrib import messages
from django.views import View
from apps.global_context import get_global_context
from apps.cart.services.cart_service import CartItemModelService
from apps.cart.dependencies import CartAppDependency
from django.http import HttpResponse
from django.middleware.csrf import get_token
from ui.components.cart.icon import cart_icon
from ui.components.cart.cart_summary import CartSummaryCard
from ui.components.cart.cart_item import CartItemRow
from django_abstract.utilities import ServiceEntryData
from apps.cart.forms.client_forms.custom_form import QuantityUpdateForm
from probo.components import frag
from probo import span

class AddToCartView(View):
    __ctx = get_global_context()

    def get(self,request,product_id):
        session_key = self.__ctx.get('session_key')
        if not session_key:
            session_key = request.sessions.session_key
            self.__ctx.put('session_key',session_key)
        quantity = request.GET.get('quantity',1)
        cart_service = CartItemModelService(session_key=session_key, load_record=False)
        entry = ServiceEntryData()
        entry.service_data["method_name"] = "add_item_to_cart"
        entry.service_data["product_variant"] = product_id
        entry.service_data["quantity"] = quantity
        # entry.service_data["cart"] = cart
        entry.service_data["session"] = session_key

        # product = get_object_or_404(ProductVariant,id=product_id)
        # cart_item,created = CartItem.objects.get_or_create(cart=cart,product_variant=product)
        # if not created:
        #     cart_item.quantity += quantity
        #     cart_item.save()
        data = cart_service.hook(entry=entry)
        self.__ctx.put("cart_item_count", data.service_data.get("total_items"))
        created =  data.service_data.get('created')
        if created:
            messages.success(request=request,message="Youre item is created successfully")
        else:
            messages.warning(request=request,message="Youre item was not created successfully")
        message = get_messages(messages=messages.get_messages(request=request))
        return HttpResponse(message.render() + cart_icon(cart_count=self.__ctx.get("cart_item_count"),hx_oob=True).render())

class RemoveFromCartView(View):
    __ctx = get_global_context()

    def get(self,request,item_id):
        session_key = self.__ctx.get('session_key')
        if not session_key:
            session_key = request.sessions.session_key
            self.__ctx.put('session_key',session_key)
        cart_service = CartItemModelService(session_key=session_key, load_record=False)
        entry = ServiceEntryData()
        entry.service_data["method_name"] = "remove_item_from_cart"
        entry.service_data["pk"] = item_id
        entry.service_data["session"] = session_key
        data = cart_service.hook(entry=entry)
        
        with self.__ctx as ctx:
            ctx.put(
                "cart_item_count", data.service_data.get("total_items")
            )
            ctx.push(**data.service_data)
            messages.success(request=request,message="Youre item is removed cessess fully")
            message = get_messages(messages=messages.get_messages(request=request),hx_oob=True)
            summary = CartSummaryCard(data.service_data.get('cart'),hx_oob=True)

            return HttpResponse(message.render() + cart_icon(cart_count=self.__ctx.get("cart_item_count"),hx_oob=True).render()+ summary.render())

class UpdateItemQuantityView(View):
    __ctx = get_global_context()

    def get(self,request,item_id):
        session_key = self.__ctx.get('session_key')
        if not session_key:
            session_key = request.sessions.session_key
            self.__ctx.put('session_key',session_key)
        cart_service = CartItemModelService(session_key=session_key, load_record=False)
        entry = ServiceEntryData()
        entry.service_data["method_name"] = "get_item"
        entry.service_data["pk"] = item_id
        data = cart_service.hook(entry=entry)
        form = QuantityUpdateForm(
            initial={"quantity": data.service_data.get("item").quantity},
            max_stock=data.service_data.get("item").product_variant.stock,
        )
        with self.__ctx as ctx:
            ctx.put("qty_form_html", str(form))
            ctx.put("csrf_token", get_token(request))
            ctx.push(**data.service_data)
            item_row = CartItemRow(data.service_data.get("item"),edit=True)
            return HttpResponse(item_row.render())

    def post(self,request,item_id):
        session_key = self.__ctx.get('session_key')
        if not session_key:
            session_key = request.sessions.session_key
            self.__ctx.put('session_key',session_key)
        form = QuantityUpdateForm(request.POST)
        qty = None
        if form.is_valid():
            qty = form.cleaned_data.get('quantity')
        cart_service = CartItemModelService(session_key=session_key, load_record=False)
        entry = ServiceEntryData()
        entry.service_data["method_name"] = "update_item_quantity"
        entry.service_data["pk"] = item_id
        entry.service_data["quantity"] = qty
        entry.service_data["session"] = session_key
        data = cart_service.hook(entry=entry)

        with self.__ctx as ctx:
            ctx.put(
                "cart_item_count", data.service_data.get("total_items")
            )
            ctx.push(**data.service_data)

            messages.success(request=request,message="Your item's quantity is updated cessess fully")
            message = get_messages(messages=messages.get_messages(request=request),hx_oob=True)
            summary = CartSummaryCard(data.service_data.get('cart'),hx_oob=True)
            item_row = span(data.service_data.get("item").quantity, Class="fw-semibold")
            return HttpResponse(frag(
                message,
                summary,
                item_row,))
