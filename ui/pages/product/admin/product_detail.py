from probo import DIV
from ui.components.product.admin.product_details import AdminProductDetailCard
from ui.pages.base import get_management_base_template
from apps.global_context import get_global_context

def AdminProductDetailPage(product=None) -> DIV:
    """
    A compact, data-rich card for admin product management.
    Expected product dict: {'name', 'sku', 'price', 'stock', 'is_active', 'image_url'}
    """
    Context = get_global_context()
    product = product or Context.get('product', None)
    if not product:
        return DIV("No product data available.", Class="alert alert-warning")
    # Dynamic status badge
    base = get_management_base_template()
    base_title = base.html_doc.find(lambda n:n.tag == "TITLE")
    if base_title:
        base_title.inner_html(f"Product Detail - {product.name}")
    base_bode = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if base_bode:
        base_bode.add(AdminProductDetailCard(product))
    return base
