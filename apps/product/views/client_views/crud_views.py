from ui.pages.product.client.product_catalog import ProductCatalogPage
from django.http import HttpResponse
from django.views import View
from apps.global_context import get_global_context
from apps.product.dependencies import get_product_app_dependency
from django.forms.models import model_to_dict
from apps.product.services.model_service import ProductVariantModelService
from apps.product.models import ProductImage, ProductVariant
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.views import View
from ui.pages.product.client.product_detail import ProductDetailPage


class ProductCatalogView(View):
    _dependency = get_product_app_dependency()
    _ctx = get_global_context()
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
        categpries = self._dependency.select_category.model_class.objects.filter(is_active=True)
        products = [
            process_item(item)
            for item in self._dependency.select_product_variant.model_class.objects.filter(
                is_active=True
            )
        ]
        # 2. Create the Product Catalog Page with the fetched products
        page = ProductCatalogPage(products=products, categpries=categpries)

        # 3. Render the page and return as HttpResponse
        rendered_page = page.render()
        return HttpResponse(rendered_page)

class ProductDetailView(View):
    __ctx = get_global_context()
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
        with self.__ctx as ctx:
            ctx.put("csrf_token", get_token(request))
            ui = ProductDetailPage(product)
            return HttpResponse(ui.render())
