from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ValidationError
from ui.components.checkout.order_success import (
    OrderSuccessReceipt,
)
# from ui.components.checkout.error import
from ui.components.checkout.error import (
    CheckoutError,
)
from ui.components.cart.icon import cart_icon
from ui.components.cart.cart_summary import CartSummaryCard
from ui.components.cart.cart_item import CartItemTable
from ui.components.messaging import get_messages
from django.contrib import messages
from apps.global_context import get_global_context
from probo.components import frag
# Import the Orchestrator!
from apps.checkout.services.checkout_service import CheckoutOrchestrator


class ProcessCheckoutView(View):
    """
    HTMX Endpoint that triggers the entire Checkout sequence.
    """
    __ctx = get_global_context()
    def post(self, request, *args, **kwargs):
        # 1. Ensure Session exists
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        # 2. Extract inputs from the POST request
        discount_code = request.POST.get("discount_code", False)

        # 3. Setup the Orchestrator
        orchestrator = CheckoutOrchestrator(session_key=session_key)

        # Load the payload into the ServiceEntryData envelope
        orchestrator.entry.service_data.update(
            {
                "method_name": "process_checkout",
                "applied_discount_code": discount_code,
                "session_key": session_key,
            }
        )

        try:
            # 4. EXECUTE!
            success = orchestrator.hook()

            if success:
                # Extract the created objects from the Orchestrator's state
                order = success.service_data.get("order")
                checkout_obj = success.service_data.get("checkout")
                cart = success.service_data.get('cart')
                total_items = success.service_data.get('total_items')
                cart_items = success.service_data.get('cart_items')
                # Render the Success Receipt Component
                self.__ctx.put("cart_item_count",total_items)
                ui = OrderSuccessReceipt(order=order, checkout_session=checkout_obj)
                summary_ui = CartSummaryCard(cart=cart,hx_oob=True)
                cart_icon_ui = cart_icon(total_items, hx_oob=True)
                messages.success(request=request,message="Operation is Proccessed SmoOothly!!")
                message_ui = get_messages(messages=messages.get_messages(request=request),hx_oob=True)

                items_table_ui = CartItemTable(cart_items, hx_oob=True)
                return HttpResponse(
                    frag(ui, cart_icon_ui, summary_ui, message_ui, items_table_ui,)
                )
            else:
                # If it failed silently without an exception
                ui = CheckoutError(
                    "Something went wrong processing your order. Please try again."
                )
                return HttpResponse(ui.render())

        except ValidationError as e:
            # Catch specific business logic errors (e.g., "Cannot checkout empty cart")
            ui = CheckoutError(
                str(e.message if hasattr(e, "message") else e.messages[0])
            )
            return HttpResponse(ui.render())

        except Exception as e:
            # Catch DB crashes or other fatal errors
            ui = CheckoutError(
                "A critical system error occurred. You have not been charged."
            )
            return HttpResponse(ui.render())
