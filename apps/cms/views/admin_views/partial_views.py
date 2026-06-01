from time import timezone
from django.urls import reverse
from django.views import View
from probo.components import frag
from probo.utility import ProboSourceString
from apps.cms.dependencies import get_cms_app_dependency
from apps.cms.forms.admin_forms.model_form import SystemBannerRotationForm
from apps.utility import CustomAdminRequiredMixin
from ui.components.cms.admin.dashboard_v2 import MediaAdminCard, render_media_grid
from apps.global_context import get_global_context
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from ui.components.messaging import get_messages
from django_abstract.utilities import AdminOrStaffMixin, HtmxLoginRequiredMixin, to_snake_case
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
                ui = MediaAdminCard(
                    obj.title if hasattr(obj, "title") else obj.customer_name if hasattr(obj, "customer_name") else obj.name if hasattr(obj, "name") else "Untitled",
                    obj.subtitle if hasattr(obj, "subtitle") else obj.description if hasattr(obj, "description") else obj.content if hasattr(obj, "content") else "No description",
                    obj.image.url if hasattr(obj, "image") else obj.customer_image.url if hasattr(obj, "customer_image") else None,
                    obj.is_active,
                    obj_id=obj.id,
                    slug=f"select_{to_snake_case(obj.__class__.__name__)}",
                )
                messages.success(
                    request,
                    f"{select_slug[7:].replace('_', ' ').capitalize()} {'Published' if obj.is_active else 'Hidden'} successfully.",
                )
                message = get_messages(messages=messages.get_messages(request),hx_oob=True)
                return HttpResponse(frag(
                    ui,
                    message,
                ))

        messages.error(request, f"{select_slug[7:].replace('_', ' ').capitalize()} not found.")
        message = get_messages(
            messages=messages.get_messages(request), hx_oob=True
            )
        return HttpResponse(
            frag(
                message,
            )
        )


class EditMediaAdminCardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()
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
                messages.success(request, f"{select_slug[7:].replace('_', ' ').capitalize()} edit functionality is started.")
                message = get_messages(messages=messages.get_messages(request), hx_oob=True)
                form_modal = AdminForm(
                    form=ProboSourceString(form),
                    action="#",
                    hx_post=reverse(
                        "cms:admin-edit-media",
                        kwargs={"slug": select_slug, "id": obj_id},
                    ),
                    hx_target="#admin-edit-modal-body",  # Swaps just this card!
                    hx_swap="innerHTML",
                )
                return HttpResponse(frag(
                    message,
                    form_modal
                ))

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
                    message = get_messages(
                        messages=messages.get_messages(request), hx_oob=True
                    )
                    form_modal = FormConfirmation()
                    return HttpResponse(frag(message, form_modal))
                else:
                    messages.error(request, f"Error updating {select_slug[7:].replace('_', ' ').capitalize()}. Please check the form for errors.")
                    message = get_messages(messages=messages.get_messages(request), hx_oob=True)
                    form_modal = AdminForm(form=form,action=reverse("cms:admin-edit-media", kwargs={"slug":select_slug, "id":obj_id}))
                    return HttpResponse(frag(
                        message,
                        form_modal
                    ))              
        messages.error(request, " invalid arguments.")
        message = get_messages(messages=messages.get_messages(request), hx_oob=True)
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
                ui = MediaAdminCard(
                    obj.title if hasattr(obj, "title") else obj.customer_name if hasattr(obj, "customer_name") else obj.name if hasattr(obj, "name") else "Untitled",
                    obj.subtitle if hasattr(obj, "subtitle") else obj.description if hasattr(obj, "description") else obj.content if hasattr(obj, "content") else "No description",
                    obj.image.url if hasattr(obj, "image") else obj.customer_image.url if hasattr(obj, "customer_image") else None,
                    obj.is_active,
                    obj_id=obj.id,
                    slug=f"select_{to_snake_case(obj.__class__.__name__)}",
                )
                messages.success(
                    request,
                    f"{select_slug[7:].replace('_', ' ').capitalize()} deleted successfully.",
                )
                message = get_messages(messages=messages.get_messages(request),hx_oob=True)
                return HttpResponse(frag(
                    ui,
                    message,
                ))

        messages.error(request, f"{select_slug[7:].replace('_', ' ').capitalize()} not found.")
        message = get_messages(
            messages=messages.get_messages(request), hx_oob=True
            )
        return HttpResponse(
            frag(
                message,
            )
        )
