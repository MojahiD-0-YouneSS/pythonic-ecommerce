from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from apps.client.systems.system import ClientSystem
from ui.components.client.profile import (
    ProfileInfoSection,
    SecuritySection,
)
from django.forms.models import model_to_dict
from django_abstract.utilities import Entry
from django.urls import reverse
from probo.request import RequestDataTransformer
from probo.components import frag,Frag

class ClientProfileInfoView(View):
    """Handles Get, Post (Create), and Put (Update) for Client Profiles."""

    def get(self, request, *args, **kwargs):

        user_data = model_to_dict(request.user)
        with request.ui_context as ctx:
            ui = ProfileInfoSection()
            ctx.push(**{'user_data': user_data, 'is_disabled': bool(kwargs.get("is_disabled",1))})
            return HttpResponse(frag(Frag(ui, data_pipeline=ctx)))

    def post(self, request, *args, **kwargs):
        entry = Entry(
            session_key=request.session.session_key,
            request=request,
        )
        
        ced = entry.control_entry_data
        sed = entry.service_entry_data
        ced.service_name = "auth_service"
        ced.service_args["session_key"] = entry.session_key
        sed.service_data["method_name"] = "update_user_info"
        sed.service_data["pk"] = request.user.id
        sed.service_data["email"] = request.user.email
        
        sed.service_data.update(RequestDataTransformer(request).post_data)

        # ClientSystem()

        system = ClientSystem(entry=entry)
        success, entry = system.execute("client_operator")
        with request.ui_context as ctx:
            ctx.push(**{'user_data': entry.service_entry_data.service_data, 'is_disabled': bool(kwargs.get("is_disabled", 1))})
            ui = ProfileInfoSection()
            return HttpResponse(frag(Frag(ui,data_pipeline=ctx)))

class ClientLoginInfoView(View):
    """Handles Get, Post (Create), and Put (Update) for Client Profiles."""

    def get(self, request, *args, **kwargs):

        user_data = model_to_dict(request.user)
        with request.ui_context as ctx:

            ui = SecuritySection()
            ctx.push(**{'user_data': user_data, 'is_disabled': bool(kwargs.get("is_disabled",1))})
            return HttpResponse(frag(Frag(ui,data_pipeline=ctx)))

    def post(self, request, *args, **kwargs):

        current_password = request.POST.get("current_password")
        error = "the current password is incorrect."
        entry = Entry(
            session_key=request.session.session_key,
            request=request,
        )
        if request.user.check_password(current_password):

            ced = entry.control_entry_data
            sed = entry.service_entry_data
            ced.service_name = "auth_service"
            ced.service_args["session_key"] = entry.session_key
            sed.service_data["method_name"] = "update_user_logins"
            sed.service_data["pk"] = request.user.id
            sed.service_data.update(RequestDataTransformer(request).post_data)

            # ClientSystem()

            system = ClientSystem(entry=entry)
            success, entry = system.execute("client_operator")
            return redirect(reverse("cms:home"))
        with request.ui_context as ctx:
            ui = SecuritySection()
            ctx.push({'user_data': entry.service_entry_data.service_data, 'is_disabled': bool(kwargs.get("is_disabled", 1)), 'error': error})
            return HttpResponse(frag(Frag(ui, data_pipeline=ctx)))
