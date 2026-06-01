from probo import DIV, H2, P
from ui.components.cms.banner import HeroBanner
from ui.components.cms.home_components import (
    RenderAboutUs,
    RenderPosters,
    RenderTestimonies,
    RenderHeroBanner,
    )
from ui.components.product.product_card import ProductCard
from ui.pages.base import get_client_base_template

class HomePage:
    def __init__(self, featured_products=None,testimnies=None,posters=None,about_us=None,banners=None):
        self._title = "Pythonic E-Commerce | Home"
        self.featured_products = featured_products or []
        self.testimnies=testimnies
        self.posters=posters
        self.about_us=about_us
        self.banners=banners
        
    def render(self):
        base = get_client_base_template()
        
        # 1. Update the Title
        base_title = base.html_doc.find(lambda n: n.tag == 'TITLE')
        if base_title:
            base_title.inner_html(self._title)
            
        # 2. Build the Page Layout (Hero + Product Grid)
        main_content = DIV(
            # Top: Hero Section
            HeroBanner() if not self.banners else RenderHeroBanner(self.banners),
            
            # Bottom: Featured Products Section
            DIV(
                DIV(
                    H2("Trending Now", Class="fw-bolder mb-4"),
                    DIV(
                        # List comprehension to generate the grid!
                        *[ProductCard(prod) for prod in self.featured_products],
                        Class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center"
                    ),
                    Class="container px-4 px-lg-5 mt-5"
                ),
                Class="py-5 bg-light"
            ),
            RenderPosters(self.posters),
            RenderTestimonies(self.testimnies),
            RenderAboutUs(self.about_us),
        )
        
        # 3. Inject into the root container (using your updated robust ID finder!)
        base_body = base.html_doc.find(lambda n: n.attr_manager.get_attr("data_ssdom_id") == 'root-container')
        if base_body:
            base_body.inner_html(main_content)
            
        return base