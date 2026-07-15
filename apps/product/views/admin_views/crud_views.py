from apps.product.models import (
    Product,
    ProductImage,
    ProductVariant,
    Category,
    ReplyModel,
    ReviewModel,
)
from apps.product.forms.admin_forms.model_form import (
    ProductModelForm,
    ProductImageModelForm,
    ProductVariantModelForm,
    CategoryModelForm,
    ReplyModelForm,
    ReviewModelForm,
)
from django.middleware.csrf import get_token
from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404,redirect
from django.http import HttpResponse
from probo.request import RequestDataTransformer
from apps.utility import CustomAdminRequiredMixin
from ui.pages.product.admin import (
    AdminProductFormPage,
    AdminProductListingPage,
    AdminProductDetailPage
    )
from probo.components import frag,Frag
from django_abstract.utilities import  HtmxLoginRequiredMixin
from probo.utility import ProboSourceString
class AddProductView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductModelForm)
        with request.ui_context as ctx:
            
            ctx.push(csrf_token=get_token(request),url='/product/add/product/',rdt_form=ProboSourceString(rdt.form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductModelForm)
        messages.success(request, "Product added successfully!")
        request.ui_context.push(django_messages=messages.get_messages(request),clear_messages=True)
        if rdt.is_valid():
            rdt.save_form()
        return redirect("product:product")

class AddProductVariantView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductVariantModelForm)

        with request.ui_context as ctx:
            ctx.push(csrf_token=get_token(request),url='/product/add/variant/',rdt_form=ProboSourceString(rdt.form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductVariantModelForm)
        if rdt.is_valid():
            rdt.save_form()
            messages.success(request, "Product Variant added successfully!")

        request.ui_context.push(django_messages=messages.get_messages(request),clear_messages=True)

        return redirect("product:variant")

class AddProductImageView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductImageModelForm)

        with request.ui_context as ctx:
            ctx.push(csrf_token=get_token(request),url='/product/add/image/',rdt_form=ProboSourceString(rdt.form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductImageModelForm)
        if rdt.is_valid():
            rdt.save_form()
            messages.success(request, "Product Image added successfully!")

        request.ui_context.push(django_messages=messages.get_messages(request),clear_messages=True)

        return redirect("product:image")

class AddProductCategoryView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=CategoryModelForm)

        with request.ui_context as ctx:
            ctx.push(csrf_token=get_token(request),url='/product/add/category/',rdt_form=ProboSourceString(rdt.form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=CategoryModelForm)
        if rdt.is_valid():
            rdt.save_form()
            messages.success(request, "Product Category added successfully!")

        request.ui_context.push(django_messages=messages.get_messages(request),clear_messages=True)

        return redirect("product:category")

class AddProductReviewView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ReviewModelForm)

        with request.ui_context as ctx:
            ctx.push(csrf_token=get_token(request),url='/product/add/review/',rdt_form=ProboSourceString(rdt.form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ReviewModelForm)
        if rdt.is_valid():
            rdt.save_form()
            messages.success(request, "Product review added successfully!")

        request.ui_context.push(django_messages=messages.get_messages(request),clear_messages=True)

        return redirect("product:review")

class AddProductReplyView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ReplyModelForm)

        with request.ui_context as ctx:
            ctx.push(csrf_token=get_token(request),url='/product/add/reply/',rdt_form=ProboSourceString(rdt.form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ReplyModelForm)
        if rdt.is_valid():
            rdt.save_form()
            messages.success(request, "Product Reply added successfully!")

        request.ui_context.push(django_messages=messages.get_messages(request),clear_messages=True)

        return redirect("product:reply")

# ==============================================================================

class ProductListView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,):
        from django.core.paginator import Paginator
        with request.ui_context as ctx:
            queryset = Product.objects.all().order_by('-id')
            page_number = request.GET.get('page', 1)
            paginator = Paginator(queryset, 12)
            page_obj = paginator.get_page(page_number)
            
            ctx.push(products=page_obj.object_list, page_obj=page_obj)
            page = AdminProductListingPage()
            page.page_obj = page_obj
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

class ProductDetailView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,product_id):
        with request.ui_context as ctx:
            product = get_object_or_404(Product, id=product_id)
            ctx.push(product=product)
            page = AdminProductDetailPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

class ProductVariantEditView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,product_id):
        product = get_object_or_404(ProductVariant, id=product_id)
        form = ProductVariantModelForm(instance=product)
        with request.ui_context as ctx:
            ctx.put('rdt_form',ProboSourceString(form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

    def post(self,request,product_id):
        form = ProductVariantModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product:products")
        with request.ui_context as ctx:
            ctx.put('rdt_form',ProboSourceString(form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

class ProductVariantDeleteView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,product_id):
        product = get_object_or_404(ProductVariant, id=product_id)
        product.is_active=False
        product.is_disabled=True
        product.is_deactivated=True
        product.save()
        return HttpResponse(frag())
    
class ProductEditView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)
        form = ProductModelForm(instance=product)
        with request.ui_context as ctx:
            ctx.put('rdt_form',ProboSourceString(form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

    def post(self,request,product_id):
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product:products")
        with request.ui_context as ctx:
            ctx.put('rdt_form',ProboSourceString(form.as_div()))
            page = AdminProductFormPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

class ProductDeleteView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)
        product.is_active=False
        product.is_disabled=True
        product.is_deactivated=True
        product.save()
        return HttpResponse(frag())
