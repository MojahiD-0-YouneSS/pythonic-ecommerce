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
from ui.components.product.form_button import form_button, form_field_wrapper
from apps.global_context import get_global_context
from probo.components import frag
from django_abstract.utilities import AdminOrStaffMixin, HtmxLoginRequiredMixin

class AddProductView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __global_context = get_global_context()
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductModelForm)
        with self.__global_context as ctx:
            
            ctx.push(csrf_token=get_token(request),url='/product/add/product/')
            page = AdminProductFormPage(rdt.form.as_div())
        return HttpResponse(page.render())

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductModelForm)
        messages.success(request, "Product added successfully!")
        self.__global_context.push(django_messages=messages.get_messages(request),clear_messages=True)
        if rdt.is_valid():
            rdt.save_form()
        return redirect("product:product")

class AddProductVariantView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __global_context = get_global_context()
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductVariantModelForm)

        with self.__global_context as ctx: 
            ctx.push(csrf_token=get_token(request),url='/product/add/variant/',)
            page = AdminProductFormPage(rdt.form.as_div())
        return HttpResponse(page.render())

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductVariantModelForm)
        if rdt.is_valid():
            rdt.save_form()
        
        return redirect("product:variant")

class AddProductImageView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __global_context = get_global_context()
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductImageModelForm)

        with self.__global_context as ctx: 
            ctx.push(csrf_token=get_token(request),url='/product/add/image/',)
            page = AdminProductFormPage(rdt.form.as_div())
        return HttpResponse(page.render())

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ProductImageModelForm)
        if rdt.is_valid():
            rdt.save_form()
        
        return redirect("product:image")

class AddProductCategoryView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __global_context = get_global_context()
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=CategoryModelForm)

        with self.__global_context as ctx: 
            ctx.push(csrf_token=get_token(request),url='/product/add/category/',)
            page = AdminProductFormPage(rdt.form.as_div())
        return HttpResponse(page.render())

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=CategoryModelForm)
        if rdt.is_valid():
            rdt.save_form()
        
        return redirect("product:category")

class AddProductReviewView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __global_context = get_global_context()
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ReviewModelForm)

        with self.__global_context as ctx: 
            ctx.push(csrf_token=get_token(request),url='/product/add/review/',)
            page = AdminProductFormPage(rdt.form.as_div())
        return HttpResponse(page.render())

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ReviewModelForm)
        if rdt.is_valid():
            rdt.save_form()
        
        return redirect("product:review")

class AddProductReplyView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __global_context = get_global_context()
    def get(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ReplyModelForm)

        with self.__global_context as ctx: 
            ctx.push(csrf_token=get_token(request),url='/product/add/reply/',)
            page = AdminProductFormPage(rdt.form.as_div())
        return HttpResponse(page.render())

    def post(self,request,):
        rdt = RequestDataTransformer(request=request, form_class=ReplyModelForm)
        if rdt.is_valid():
            rdt.save_form()
        
        return redirect("product:reply")

# ==============================================================================

class ProductListView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __global_context = get_global_context()
    def get(self,request,):
        with self.__global_context as ctx:
            products = Product.objects.all()
            ctx.push(products=products)
            page = AdminProductListingPage()
            return HttpResponse(page.render())

class ProductDetailView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __global_context = get_global_context()
    def get(self,request,product_id):
        with self.__global_context as ctx:
            product = get_object_or_404(Product, id=product_id)
            ctx.push(product=product)
            page = AdminProductDetailPage()
            return HttpResponse(page.render())


class ProductVariantEditView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,product_id):
        product = get_object_or_404(ProductVariant, id=product_id)
        form = ProductVariantModelForm(instance=product)
        page = AdminProductFormPage(form=form.as_div())
        return HttpResponse(page.render())

    def post(self,request,product_id):
        form = ProductVariantModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product:products")

        page = AdminProductFormPage(form=form.as_div())
        return HttpResponse(page.render())

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
        page = AdminProductFormPage(form=form.as_div())
        return HttpResponse(page.render())

    def post(self,request,product_id):
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product:products")

        page = AdminProductFormPage(form=form.as_div())
        return HttpResponse(page.render())

class ProductDeleteView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self,request,product_id):
        product = get_object_or_404(Product, id=product_id)
        product.is_active=False
        product.is_disabled=True
        product.is_deactivated=True
        product.save()
        return HttpResponse(frag())
