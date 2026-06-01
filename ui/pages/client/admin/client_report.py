from ui.components.client.admin.client_report import AdminUserDetailCard
from ui.pages.base import get_management_base_template
from apps.global_context import get_global_context
from probo import DIV, H4, P, H5


def AdminUserDetailPage():
    base = get_management_base_template()
    context = get_global_context()
    client = context.get('client', None)
    base_title = base.html_doc.find(lambda n: n.tag == "TITLE")
    if base_title:
        base_title.inner_html(f'User Detail - {client.user.username if client else "Unknown User"}')
    base_body = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if base_body:
        content = AdminUserDetailCard(client.user if client else None, client)
        base_body.add(content)
    return base
