from ui.pages.base import get_management_base_template
from ui.components.order.admin.order_management import OrderManagementSection
from apps.global_context import get_global_context

def OrderManagementPage():
    template = get_management_base_template()
    ctx = get_global_context()
    template_title = template.html_doc.find(
        lambda tag: tag.tag == "TITLE"
    )
    if template_title:
        template_title.inner_html("Order Management")
    template_body = template.html_doc.find(
        lambda tag: tag.attr_manager.get_attr('data_ssdom_id') == 'root-container'
    )
    if template_body:
        template_body.add(
            OrderManagementSection(ctx.get('order'))
        )
    
    
    return template
