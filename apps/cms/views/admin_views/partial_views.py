from django.urls import reverse
from django.views import View
from probo.components import frag, Frag
from probo.utility import ProboSourceString
from apps.cms.dependencies import get_cms_app_dependency
from apps.utility import CustomAdminRequiredMixin
from ui.components.cms.admin.dashboard_v2 import MediaAdminCard
from django.http import HttpResponse
from django.contrib import messages
from ui.components.messaging import get_messages
from django_abstract.utilities import HtmxLoginRequiredMixin
from apps.cms.forms.admin_forms.model_form import (
    QuoteForm,
SystemBannerRotationForm,
HomepageEditorForm,
BannerForm,
PosterForm,
TestimonyForm,
AboutUsForm,
ContactForm,
ContactUsForm,
PageVisitForm,
DashboardMetricsForm,
)
from ui.components.shared.admin_form import AdminForm, FormConfirmation


class HideMediaAdminCardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        select_slug, obj_id = kwargs.get("slug"), kwargs.get("id")
        cmsd = get_cms_app_dependency()
        if select_slug and obj_id:

            selector_obj = getattr(cmsd, select_slug)
            if selector_obj:
                obj = selector_obj.get_by(id=obj_id)
                obj.is_active = not obj.is_active # Toggle the active state
                obj.is_disabled = False # Ensure disabled is False when toggling active
                obj.is_deactivated = False # Ensure disabled is False when toggling active
                obj.highlighted = obj.is_active
                obj.save()
                with request.ui_context as ctx:
                    ui = MediaAdminCard()
                    messages.success(
                        request,
                        f"{select_slug[7:].replace('_', ' ').capitalize()} {'Published' if obj.is_active else 'Hidden'} successfully.",
                    )
                    message = get_messages()
                    ctx.push(obj=obj,django_messages=messages.get_messages(request),hx_oob='true')
                    return HttpResponse(frag(Frag(
                        ui,
                        message,
                    )))
        with request.ui_context as ctx:
            messages.error(request, f"{select_slug[7:].replace('_', ' ').capitalize()} not found.")
            ctx.push(django_messages=messages.get_messages(request), hx_oob="true")
            message = get_messages()
            return HttpResponse(
                frag(
                    Frag(
                    message,
                    data_pipeline=ctx,
                )))

class EditMediaAdminCardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get_form_class(self, obj,instance=False):
        form_registry = {
            "Quote": QuoteForm,
            "SystemBannerRotation": SystemBannerRotationForm,
            "HomepageEditor": HomepageEditorForm,
            "Banner": BannerForm,
            "Poster": PosterForm,
            "Testimony": TestimonyForm,
            "AboutUs": AboutUsForm,
            "Contact": ContactForm,
            "ContactUs": ContactUsForm,
            "PageVisit": PageVisitForm,
            "DashboardMetrics": DashboardMetricsForm,  
        }
        return form_registry.get(obj.__class__.__name__) if not instance else form_registry.get(obj.__class__.__name__)(instance=obj)
    def get(self, request, *args, **kwargs):
        select_slug, obj_id = kwargs.get("slug"), kwargs.get("id")
        cmsd = get_cms_app_dependency()

        if select_slug and obj_id:
            selector_obj = getattr(cmsd, select_slug)
            if selector_obj:
                obj = selector_obj.get_by(id=obj_id)
                form = self.get_form_class(obj, instance=True)
                # Here you would implement the logic to edit the media object
                # For demonstration, we'll just return a success message
                with request.ui_context as ctx:
                    messages.success(request, f"{select_slug[7:].replace('_', ' ').capitalize()} edit functionality is started.")
                    ctx.push(
                        django_messages=messages.get_messages(request),
                        hx_oob='true',
                        rdt_form=ProboSourceString(form),
                        action='#',
                    )
                    message = get_messages()
                    form_modal = AdminForm()
                    form_modal.attr_manager.set_bulk_attr(
                        hx_post=reverse(
                            "cms:admin-edit-media",
                            kwargs={"slug": select_slug, "id": obj_id},
                        ),
                        hx_target="#admin-edit-modal-body",  # Swaps just this card!
                        hx_swap="innerHTML",
                    )
                    return HttpResponse(frag(Frag(
                        message,
                        form_modal,
                        data_pipeline=ctx
                )))
        with request.ui_context as ctx:

            messages.error(request, f"{select_slug[7:].replace('_', ' ').capitalize()} not found.")
            ctx.push(django_messages=messages.get_messages(request), hx_oob='true')

            message = get_messages()
            return HttpResponse(
                frag(
                   Frag(message,data_pipeline=ctx)
                )
            )
    def post(self, request, *args, **kwargs):
        select_slug, obj_id = kwargs.get("slug"), kwargs.get("id")
        cmsd = get_cms_app_dependency()
        if select_slug and obj_id:
            selector_obj = getattr(cmsd, select_slug)
            if selector_obj:
                obj = selector_obj.get_by(id=obj_id)
                form = self.get_form_class(obj=obj)(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"{select_slug[7:].replace('_', ' ').capitalize()} updated successfully.")
                    message = get_messages()
                    message.load_data({'django_messages': messages.get_messages(request), 'hx_oob': True})
                    form_modal = FormConfirmation()
                    return HttpResponse(frag(message, form_modal))
                else:
                    messages.error(request, f"Error updating {select_slug[7:].replace('_', ' ').capitalize()}. Please check the form for errors.")
                    message = get_messages()
                    message.load_data({'django_messages': messages.get_messages(request), 'hx_oob': True})
                    form_modal = AdminForm()
                    form_modal.load_data({'form': form, 'action': reverse("cms:admin-edit-media", kwargs={"slug":select_slug, "id":obj_id})})
                    return HttpResponse(frag(
                        message,
                        form_modal
                    ))              
        messages.error(request, " invalid arguments.")
        message = get_messages()
        message.load_data({'django_messages': messages.get_messages(request), 'hx_oob': True})
        return HttpResponse(frag(
            message,
        ))

class DeleteMediaAdminCardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def delete(self, request, *args, **kwargs):
        select_slug, obj_id = kwargs.get("slug"), kwargs.get("id")
        cmsd = get_cms_app_dependency()
        if select_slug and obj_id:

            selector_obj = getattr(cmsd, select_slug)
            if selector_obj:
                obj = selector_obj.get_by(id=obj_id)
                obj.is_active = False # Toggle the active state
                obj.is_disabled = True # Toggle the disabled state
                obj.is_deactivated = True # Toggle the deactivation state
                obj.save()
                with request.ui_context as ctx:
                    ctx.put('obj',obj)
                    ui = MediaAdminCard()
                    messages.success(
                        request,
                        f"{select_slug[7:].replace('_', ' ').capitalize()} deleted successfully.",
                    )
                    ctx.push(django_messages=messages.get_messages(request),hx_oob='true')
                    message = get_messages()
                    return HttpResponse(frag(Frag(
                        ui,
                        message,
                        data_pipeline=ctx
                    )))
        with request.ui_context as ctx:

            messages.error(request, f"{select_slug[7:].replace('_', ' ').capitalize()} not found.")
            ctx.push(django_messages=messages.get_messages(request), hx_oob='true')

            message = get_messages()
            return HttpResponse(
                frag(
                   Frag(message,data_pipeline=ctx)
                )
            )
