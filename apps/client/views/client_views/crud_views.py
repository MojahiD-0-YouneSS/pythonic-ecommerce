from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from apps.client.systems.system import ClientSystem
from ui.pages.client.client.auth import LoginPage, SignupPage
from ui.pages.client.client.profile import (
    ClientProfilePage,
)
from ui.components.client.profile import (
    ProfileInfoSection,
    OrderHistorySection,
    AddressBookSection,
    SecuritySection,
    )
from django.middleware.csrf import get_token
from django.urls import reverse
from probo.components import frag, Frag
from probo.request import RequestDataTransformer
from django.contrib import messages
from ui.components.messaging import get_messages
from django_abstract.utilities import Entry

def execute_client_flow(request, service, method, include_request=False, **kwargs):
    """Helper to inject targets, run the SessionFilterSystem, and format the response."""

    ced = request.django_abstract_entry.control_entry_data
    sed = request.django_abstract_entry.service_entry_data
    ced.service_name = service
    sed.service_data["method_name"] = method
    if include_request:
        kwargs["request"] = request

    if kwargs:
        request.django_abstract_entry.service_entry_data.service_data.update(kwargs)
    system = ClientSystem(entry=request.django_abstract_entry)
    success, entry = system.execute('client_operator')

    if success:
        entry.service_entry_data.service_data["request"] = 0
        if request.headers.get('HX-Request') == 'true':
            response = HttpResponse()
            response["HX-Redirect"] = reverse("cms:home")
            return response
        return redirect("cms:home")
    return JsonResponse(
        {
            "status": "error",
            "errors": {
                'service':entry.service_entry_data.errors,
                'control':entry.control_entry_data.errors,
                'entry':entry.errors,
                }
        },
        status=400,
    )

# --- AUTH VIEWS ---

class ClientLoginView(View):
    def get(self,request):
        with request.ui_context as ctx:
            ctx.put("csrf_token", get_token(request))
            ctx.put('django_messages', messages.get_messages(request))
            page = LoginPage()
            msg = get_messages()
            return HttpResponse(frag(Frag(page,Frag(msg,data_pipeline={'hx_oob','true',}),data_pipeline=ctx)))

    def post(self, request, *args, **kwargs):
        rdt = RequestDataTransformer(request=request)
        payload = {
            "username_or_email": rdt.post_data.get("email"),
            "password": rdt.post_data.get('password'),
        }
        response = execute_client_flow(
            request, "auth_service", "login_user",include_request=True, **payload
        )
        if isinstance(response, JsonResponse) and response.status_code == 400:
            import json
            try:
                error_data = json.loads(response.content)
                errors = error_data.get("errors", {}).get("service", {})
                error_msg = errors.get("auth", "Invalid credentials.") or "Login failed."
            except:
                error_msg = "Invalid credentials."
            messages.error(request, error_msg)
            return redirect("client:login")
        return response

class ClientSignupView(View):

    def get(self, request):
        with request.ui_context as ctx:
            ctx.put("csrf_token", get_token(request))
            ctx.put('django_messages', messages.get_messages(request))

            page = SignupPage()
            msg = get_messages()

            return HttpResponse(frag(Frag(page, Frag(msg, data_pipeline={'hx_oob', 'true', }), data_pipeline=ctx)))

    def post(self, request, *args, **kwargs):
        # Assumes create_entry handles registration in ClientModelService
        rdt = RequestDataTransformer(request=request)

        payload = {
            "username": rdt.post_data.get("username"),
            "email": rdt.post_data.get("email"),
            "password": rdt.post_data.get("password"),
            "first_name": rdt.post_data.get("first_name"),
            "last_name": rdt.post_data.get("last_name"),
            "service_args": {"session_key": request.session.session_key,
                             "load_record":False,
                             
                             },
        }
        response = execute_client_flow(request, "auth_service", "register_user", include_request=True, **payload)
        if isinstance(response, JsonResponse) and response.status_code == 400:
            import json
            try:
                error_data = json.loads(response.content)
                errors = error_data.get("errors", {}).get("service", {})
                error_msg = list(errors.values())[0] if errors else "Registration failed."
            except:
                error_msg = "Registration failed."
            messages.error(request, error_msg)
            return redirect("client:signup")
        return response

class ClientLogoutView(View):
    def get(self, request, *args, **kwargs):
        return execute_client_flow(request, "auth_service", "logout_user", include_request=True)
    def post(self, request, *args, **kwargs):
        return execute_client_flow(request, "auth_service", "logout_user", include_request=True)

# --- PROFILE VIEWS ---

class ClientProfileView(View):
    """Handles Get, Post (Create) for Client Profiles."""

    def get(self, request, *args, **kwargs):

        entry = Entry(
            session_key=request.session.session_key,
            request=request,
            )
        ced = entry.control_entry_data
        sed = entry.service_entry_data
        ced.service_name = 'user_model_service'
        ced.service_args["session_key"] = entry.session_key
        ced.service_args["load_record"] = False

        sed.service_data["method_name"] = 'read_entry'
        sed.service_data["pk"] = request.user.id
        # ClientSystem()

        system = ClientSystem(entry=entry)
        success, entry = system.execute('client_operator')
        if success:
            with request.ui_context as ctx:

                profile_section = ProfileInfoSection()
                ctx.push(**{'user_data': entry.service_entry_data.service_data,'active_tab_html':profile_section})
                ui = ClientProfilePage()
                return HttpResponse(frag(Frag(ui, data_pipeline=ctx)))
        return redirect('client:login')


# --- SHOPPING HISTORY VIEWS ---


class ShoppingHistoryView(View):
    """Read-only view for shopping history on the client side."""

    def get(self, request, *args, **kwargs):
        # Depending on your base service, this might be list_entries or read_entry
        # kwargs.update({
        #     "service_args": {"session_key": request.session.session_key,
        #                      }}
        # )
        return execute_client_flow(
            request, "shopping_history_model_service", "read_entry",**kwargs
        )
