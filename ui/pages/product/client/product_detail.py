from probo import DIV, TEXT, IMG, BUTTON, FORM, INPUT
from  ui.pages.base import get_client_base_template
from ui.components.product.client.product_detail import ProductDetail

def ProductDetailPage(product):
    """
    Displays a single product and handles the 'Add to Cart' HTMX interaction.
    """
    base = get_client_base_template()
    base.html_doc.find(lambda n:n.tag == 'TITLE').inner_html('Detail page')
    container = base.html_doc.find(lambda n:n.attr_manager.get_attr('data_ssdom_id') == 'root-container')
    if container:
        container.add(ProductDetail(product))

    return base
