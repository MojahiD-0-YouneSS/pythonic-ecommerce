# from ui.components.cms.admin.site_content_dashboard import SiteContentDashboard
from ui.components.cms.admin.dashboard_v2 import SiteContentDashboard
from apps.global_context import get_global_context
from ui.pages.base import get_management_base_template


def SiteContentPage():
    __ctx = get_global_context()
    base =  get_management_base_template()
    base_title = base.html_doc.find(lambda n:n.tag == "TITLE")
    if base_title:
        base_title.inner_html("Site Dashboard")
    base_body = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if base_body:
        base_body.add(SiteContentDashboard(__ctx))
    return base
