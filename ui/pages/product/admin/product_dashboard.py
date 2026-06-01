from ui.pages.base import get_management_base_template
from ui.components.product.admin.products_dashboard import AdminProductsDashboard
from apps.global_context import get_global_context
from probo import DIV

def product_dashboard_page():
    Context = get_global_context()
    products = Context.get('products', None)
    if not products:
        return DIV("No product data available.", Class="alert alert-warning")
    # Dynamic status badge
    base = get_management_base_template()
    base_title = base.html_doc.find(lambda n:n.tag == "TITLE")
    if base_title:
        base_title.inner_html(f"Product Dashboard - ")
    base_body = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if base_body:
        base_body.add(AdminProductsDashboard(products=products))
    return base
