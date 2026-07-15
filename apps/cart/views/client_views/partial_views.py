from probo.utility import ProboSourceString
from ui.components.messaging import get_messages
from django.contrib import messages
from django.views import View
from apps.cart.services.cart_service import CartItemModelService
from apps.cart.dependencies import CartAppDependency
from django.http import HttpResponse
from django.middleware.csrf import get_token
from ui.components.cart.icon import cart_icon
from ui.components.cart.cart_summary import CartSummaryCard
from ui.components.cart.cart_item import CartItemRow
from django_abstract.utilities import ServiceEntryData
from apps.cart.forms.client_forms.custom_form import QuantityUpdateForm
from probo.components import frag, Frag
from probo import span

class AddToCartView(View):

    def get(self,request,product_id):
        session_key = request.ui_context.get('session_key')
        if not session_key:
            session_key = request.sessions.session_key
            request.ui_context.put('session_key',session_key)
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
        with request.ui_context as ctx:
            ctx.put("cart_item_count", data.service_data.get("total_items"))
            ctx.put("hx_oob", "true")
            created =  data.service_data.get('created')
            if created:
                messages.success(request=request,message="Youre item is created successfully")
            else:
                messages.warning(request=request,message="Youre item was not created successfully")
            ctx.put('django_messages',messages.get_messages(request=request))
            message = get_messages()
            return HttpResponse(frag(Frag(message, cart_icon(),data_pipeline=ctx)))

class RemoveFromCartView(View):

    def get(self,request,item_id):
        session_key = request.ui_context.get('session_key')
        if not session_key:
            session_key = request.sessions.session_key
            request.ui_context.put('session_key',session_key)
        cart_service = CartItemModelService(session_key=session_key, load_record=False)
        entry = ServiceEntryData()
        entry.service_data["method_name"] = "remove_item_from_cart"
        entry.service_data["pk"] = item_id
        entry.service_data["session"] = session_key
        data = cart_service.hook(entry=entry)
        
        with request.ui_context as ctx:
            ctx.put(
                "cart_item_count", data.service_data.get("total_items")
            )
            ctx.put(
                "hx_oob", "true"
            )
            ctx.push(**data.service_data)
            messages.success(request=request,message="Your item is removed successfully")
            message = get_messages()
            summary = CartSummaryCard()

            return HttpResponse(frag(Frag(message , cart_icon(), summary,data_pipeline=ctx)))

class UpdateItemQuantityView(View):

    def get(self,request,item_id):
        session_key = request.ui_context.get('session_key')
        if not session_key:
            session_key = request.sessions.session_key
            request.ui_context.put('session_key',session_key)
        cart_service = CartItemModelService(session_key=session_key, load_record=False)
        entry = ServiceEntryData()
        entry.service_data["method_name"] = "get_item"
        entry.service_data["pk"] = item_id
        data = cart_service.hook(entry=entry)
        form = QuantityUpdateForm(
            initial={"quantity": data.service_data.get("item").quantity},
            max_stock=data.service_data.get("item").product_variant.stock,
        )
        with request.ui_context as ctx:
            ctx.put("qty_form", ProboSourceString(form))
            ctx.put("csrf_token", get_token(request))
            ctx.push(**data.service_data)
            ctx.put('edit',True)
            item_row = CartItemRow()

            return HttpResponse(frag(Frag(item_row,data_pipeline=ctx)))

    def post(self,request,item_id):
        session_key = request.ui_context.get('session_key')
        if not session_key:
            session_key = request.sessions.session_key
            request.ui_context.put('session_key',session_key)
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

        with request.ui_context as ctx:
            ctx.put(
                "cart_item_count", data.service_data.get("total_items")
            )
            ctx.push(**data.service_data)
            ctx.put('hx_oob','true')

            messages.success(request=request,message="Your item's quantity is updated successfully")
            ctx.put('django_messages',messages.get_messages(request))
            message = get_messages()
            summary = CartSummaryCard()
            item_row = span(data.service_data.get("item").quantity, Class="fw-semibold")

            return HttpResponse(frag(Frag(
                message,
                summary,
                item_row,data_pipeline=ctx),))
