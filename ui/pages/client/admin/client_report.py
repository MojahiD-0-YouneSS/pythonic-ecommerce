from ui.components.client.admin.client_report import AdminUserDetailCard
from ui.pages.base import get_management_base_template
from probo import DIV, H4, P, H5


def AdminUserDetailPage():
    base = get_management_base_template()

    base_title = base.html_doc.find(lambda n: n.tag == "TITLE")
    if base_title:
        base_title.inner_html({'client',lambda **dvars:f'User Detail - {dvars.get("client").user.username if dvars.get("client",None) else "Unknown User"}'})
    base_body = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if base_body:
        content = AdminUserDetailCard()
        base_body.add(content)
    return base
