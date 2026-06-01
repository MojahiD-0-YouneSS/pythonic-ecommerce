from ui.components.client.profile import (
    ClientProfile
)
from ui.pages.base import get_client_base_template
from apps.global_context import get_global_context


def ClientProfilePage(*args,**kwargs):
    base = get_client_base_template()
    ctx = get_global_context()
    container = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if container:
        container.add(ClientProfile(*args))
    return base
