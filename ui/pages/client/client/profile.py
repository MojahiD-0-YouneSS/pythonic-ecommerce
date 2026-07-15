from ui.components.client.profile import (
    ClientProfile
)
from ui.pages.base import get_client_base_template

def ClientProfilePage():
    base = get_client_base_template()
    container = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if container:
        profile = ClientProfile()
        container.add(profile)
    return base
