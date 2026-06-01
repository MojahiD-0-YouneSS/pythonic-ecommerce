from ui.pages.base import get_management_base_template
from apps.global_context import get_global_context
from probo import DIV,P
from ui.components.cms.admin import get_admin_dashboard

def DashboardPage():
    
    base =  get_management_base_template()
    base_title = base.html_doc.find(lambda n:n.tag == "TITLE")
    if base_title:
        base_title.inner_html("Dashboard")
    base_body = base.html_doc.find(lambda n:n.attr_manager.get_attr('data_ssdom_id') == "root-container")
    if base_body:
        
        base_body.add(get_admin_dashboard())
    return base