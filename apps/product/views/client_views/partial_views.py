from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.forms.models import model_to_dict
from apps.product.models import ProductVariant
from probo.components import frag,Frag
from ui.components.product.client.product_catalog import ProductsSection
from apps.product.models import ProductImage

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
                image = ProductImage.objects.filter(variant=product).first()
                product_dict = model_to_dict(product)
                product_dict['image_url'] = image.image if image else None
                product_dict['id']=product.id
                product_dict['name']=product.product.name
                return product_dict

            from django.core.paginator import Paginator
            queryset = products.order_by('-id')
            page_number = request.GET.get('page', 1)
            paginator = Paginator(queryset, 12)
            page_obj = paginator.get_page(page_number)
            
            products_list = [process(p) for p in page_obj.object_list]
        else:
            products_list=[]
            page_obj = None
        with request.ui_context as ctx:
            query_dict = request.GET.copy()
            if 'page' in query_dict:
                del query_dict['page']
            
            ctx.push(products=products_list, page_obj=page_obj, query_string=query_dict.urlencode())
            html = ProductsSection()
            return HttpResponse(frag(Frag(html,data_pipeline=ctx)))
