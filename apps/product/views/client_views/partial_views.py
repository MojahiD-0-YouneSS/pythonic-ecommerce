from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.forms.models import model_to_dict
from apps.product.models import ProductVariant
from ui.components.product.client.category_filter import (
    CategoryFilterSidebar,
)
from ui.components.product.client.product_catalog import ProductCatalog, ProductsSection
from apps.product.models import ProductImage,Category, Product

class ProductFilterView(View):
    def get(self,request):
        # 1. Capture selected filters from GET parameters (?category=1&category=2...)
        selected_categories = request.GET.getlist("category")
        # 2. Query products based on the selection
        products = ProductVariant.objects.all()

        if selected_categories and "clear" not in request.GET:

            products = products.filter(product__categories__id__in=selected_categories)

        # 3. If it's an HTMX partial swap, just return the grid inside the container

        if products:
            def process(product):
                image = ProductImage.objects.get(variant=product).image
                product_dict = model_to_dict(product)
                product_dict['image_url']=image
                product_dict['id']=product.id
                product_dict['name']=product.product.name
                return product_dict

            products_list = [process(p) for p in products]

            html = ProductsSection(products_list, hx_oob=True).render() 
        return HttpResponse(html)
