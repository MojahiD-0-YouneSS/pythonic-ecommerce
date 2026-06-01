from django.http import HttpResponse
from ui.pages.cms.client.home import HomePage
from django.views import View
from apps.cms.dependencies import CmsAppDependency
from apps.product.dependencies import ProductAppDependecy
# from apps.cms.services.cms_/model_service import (
#     BannerModelService,
#     TestimonyModelService,
#     PosterModelService,

# )

class HomePageView(View):
    def get(self,request):
        # Dummy data for the MVP. Later, this will be: Product.objects.filter(is_featured=True)[:4] id
        PAD = ProductAppDependecy()
        products = PAD.select_product_variant.model_class.objects.filter(
            is_active=True, is_deactivated=False, is_disabled=False
        ).distinct()
        dummy_products = [
            {
                "id": pv.id,
                "name": pv.product.name,
                "price":pv.base_price,
                "image_url": PAD.select_product_image.model_class.objects.filter(variant=pv).first().image,
            }
            for pv in (products if len(products) <= 6 else products[:4])
        ]
        CMS = CmsAppDependency()
        posters = CMS.select_poster.model_class.objects.filter(is_active=True,is_featured=True,is_deactivated=False,is_disabled=False)
        banners = CMS.select_banner.model_class.objects.filter(is_active=True,is_featured=True,is_deactivated=False,is_disabled=False)
        testimonies = CMS.select_testimony.model_class.objects.filter(
            is_active=True, highlighted=True, is_deactivated=False, is_disabled=False
        )
        ui_tree = HomePage(featured_products=dummy_products,posters=[p.__dict__ for p in (posters if len(posters)<=6 else posters[:6])],testimnies=[t.__dict__ for t in (testimonies if len(testimonies)<=6 else testimonies[:6])],banners=[b.__dict__ for b in (banners if len(banners)<=6 else banners[:6])]).render()
        return HttpResponse(ui_tree.render())
