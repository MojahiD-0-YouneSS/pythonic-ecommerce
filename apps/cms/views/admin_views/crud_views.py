from apps.utility import CustomAdminRequiredMixin
from ui.pages.cms.admin.generic_content_form import AdminGenericFormPage
from django.views import View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from apps.cms.forms.admin_forms.model_form import (
    BannerForm, PosterForm, SystemBannerRotationForm, TestimonyForm, AboutUsForm
)
from django_abstract.utilities import AdminOrStaffMixin, HtmxLoginRequiredMixin
from probo.components import frag, Frag

class AdminBannerCreateView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self, request):
        form = BannerForm()
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add New Banner")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))
            
    def post(self, request):
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner added successfully!")
            request.ui_context.push(django_messages=messages.get_messages(request), clear_messages=True)
            return redirect('cms:admin-site-content')
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add New Banner")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))

class AdminPosterCreateView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self, request):
        form = PosterForm()
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add New Poster")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))
            
    def post(self, request):
        form = PosterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Poster added successfully!")
            request.ui_context.push(django_messages=messages.get_messages(request), clear_messages=True)
            return redirect('cms:admin-site-content')
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add New Poster")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))

class AdminSystemBannerCreateView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self, request):
        form = SystemBannerRotationForm()
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add System Banner")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))
            
    def post(self, request):
        form = SystemBannerRotationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "System Banner added successfully!")
            request.ui_context.push(django_messages=messages.get_messages(request), clear_messages=True)
            return redirect('cms:admin-site-content')
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add System Banner")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))

class AdminTestimonyCreateView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self, request):
        form = TestimonyForm()
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add Testimony")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))
            
    def post(self, request):
        form = TestimonyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimony added successfully!")
            request.ui_context.push(django_messages=messages.get_messages(request), clear_messages=True)
            return redirect('cms:admin-site-content')
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add Testimony")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))

class AdminAboutUsCreateView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self, request):
        form = AboutUsForm()
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add About Us Section")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))
            
    def post(self, request):
        form = AboutUsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "About Us Section added successfully!")
            request.ui_context.push(django_messages=messages.get_messages(request), clear_messages=True)
            return redirect('cms:admin-site-content')
        with request.ui_context as ctx:
            ctx.put("action", request.path)
            ctx.put("rdt_form", form)
            page = AdminGenericFormPage("Add About Us Section")
            return HttpResponse(frag(Frag(page, data_pipeline=ctx)))
