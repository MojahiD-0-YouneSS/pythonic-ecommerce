from ui.components.product.admin import AdminProductList
from ui.pages.base import get_management_base_template
from probo import DIV

def AdminProductListingPage(*args,**kwargs):
    base = get_management_base_template()
    base_title = base.html_doc.find(lambda n:n.tag == "TITLE")
    if base_title:
        base_title.inner_html('Product Listing!')

    base_bode = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if base_bode:
        base_bode.add(DIV(AdminProductList(),Class="p-5"))
    return base
