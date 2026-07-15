from ui.pages.base import get_management_base_template
from ui.components.order.admin.order_management import OrderManagementSection

def OrderManagementPage():
    template = get_management_base_template()
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
            OrderManagementSection()
        )
    
    
    return template
