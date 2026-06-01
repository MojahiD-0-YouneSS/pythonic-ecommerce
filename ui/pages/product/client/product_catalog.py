from ui.pages.base import get_client_base_template 
from probo import DIV, H1, UL, LI
from ui.components.product.client.product_catalog import ProductCatalog

class ProductCatalogPage:
    def __init__(self, products=None,categpries=None):
        self.template = get_client_base_template()
        self.products = products or []
        self.categpries = categpries or []
        self._title = "This is the product catalog page."

    def render(self):
        # 1. Update the Title
        base_title = self.template.html_doc.find(lambda n: n.tag == 'TITLE')
        if base_title:
            base_title.inner_html(self._title)

        # 2. Build the Product Catalog Layout (for now, just a simple list)
        product_list = ProductCatalog(self.products, self.categpries)

        # 3. Inject into the root container
        root_container = self.template.html_doc.find(lambda n: n.attr_manager.get_attr("data_ssdom_id") == 'root-container')
        if root_container:
            root_container.add(DIV(product_list))

        return self.template.render()
