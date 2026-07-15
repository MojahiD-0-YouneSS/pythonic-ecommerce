from ui.pages.product.client.product_catalog import ProductCatalogPage
from apps.product.dependencies import get_product_app_dependency
from django.forms.models import model_to_dict
from apps.product.services.model_service import ProductVariantModelService
from apps.product.models import ProductImage
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.views import View
from ui.pages.product.client.product_detail import ProductDetailPage
from probo.components import frag,Frag

class ProductCatalogView(View):
    _dependency = get_product_app_dependency()
    def get(self, request):
        # 1. Fetch products from the database (for now, we'll use dummy data)
        def process_item(item):
            obj_dict = model_to_dict(item)
            obj_dict.update(
                {
                    "image_url": self._dependency.select_product_image.model_class.objects.filter(
                        variant=item
                    )
                    .first()
                    .image,
                    'name':item.product.name,
                    'id':item.id
                }
            )
            return obj_dict
        from django.core.paginator import Paginator
        categories = self._dependency.select_category.model_class.objects.filter(is_active=True)
        queryset = self._dependency.select_product_variant.model_class.objects.filter(is_active=True).order_by('-id')
        
        page_number = request.GET.get('page', 1)
        paginator = Paginator(queryset, 12)
        page_obj = paginator.get_page(page_number)
        
        products = [
            process_item(item)
            for item in page_obj.object_list
        ]

        page = ProductCatalogPage(products=products, categories=categories)
        page.page_obj = page_obj
        
        query_dict = request.GET.copy()
        if 'page' in query_dict:
            del query_dict['page']
        page.query_string = query_dict.urlencode()
        
        return HttpResponse(frag(page,))

class ProductDetailView(View):
    def get(self, request, product_id,*args, **kwargs):
        product_variant_service = ProductVariantModelService(
            session_key=request.session.session_key,id=product_id
        )
        product = model_to_dict(product_variant_service.db_record)
        product['name'] =product_variant_service.db_record.product.name
        product['description'] =product_variant_service.db_record.product.description
        product['id'] =product_variant_service.db_record.id
        product["features"] = product_variant_service.db_record.product.variants.all()
        product['image_url']=ProductImage.objects.get(variant=product_variant_service.db_record).image
        with request.ui_context as ctx:
            ctx.put("csrf_token", get_token(request))
            ctx.put("product", product)
            ui = ProductDetailPage()
            return HttpResponse(frag(Frag(ui, data_pipeline=ctx)))
