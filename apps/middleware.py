import traceback
import logging
from django.http import HttpResponse
from django.contrib import messages
from probo.components import frag, Frag
from ui.components.messaging import get_messages

logger = logging.getLogger(__name__)

class HTMXErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # 1. Diagnostics: Always log the error
        logger.error(f"Unhandled Exception: {exception}\n{traceback.format_exc()}")
        
        # 2. Error Handling: Graceful fail for HTMX
        if request.headers.get("HX-Request") == "true":
            messages.error(request, f"An unexpected error occurred: {str(exception)}")
            
            if hasattr(request, "ui_context"):
                with request.ui_context as ctx:
                    ctx.put('django_messages', messages.get_messages(request))
                    ctx.put('clear_messages', True)
                    ctx.put('hx_oob', "true")
                    return HttpResponse(frag(Frag(get_messages(), data_pipeline=ctx)))
            else:
                # Fallback if ui_context is missing
                return HttpResponse(
                    f'<div id="messages-container" hx-swap-oob="true" class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 1055;"><div class="alert alert-danger">{str(exception)}</div></div>', 
                    status=200
                )
                
        # Return None lets Django's standard 500 HTML view handle it for non-HTMX requests.
        return None
