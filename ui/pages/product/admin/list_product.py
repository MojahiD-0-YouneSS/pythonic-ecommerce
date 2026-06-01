from ui.components.product.admin import AdminProductList
from ui.pages.base import get_management_base_template
from apps.global_context import get_global_context
from probo import DIV

def AdminProductListingPage(*args,**kwargs):
    Context = get_global_context()
    base = get_management_base_template()
    products = Context.get('products',[])
    base_title = base.html_doc.find(lambda n:n.tag == "TITLE")
    if base_title:
        base_title.inner_html('Product Listing!')

    base_bode = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if base_bode:
        base_bode.add(DIV(AdminProductList(products,),Class="p-5"))
    return base
