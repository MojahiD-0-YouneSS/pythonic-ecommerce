from ui.components.client.auth import (
    SignupForm,
    LoginForm,
)
from ui.pages.base import get_client_base_template
from apps.global_context import get_global_context

def LoginPage():
    base = get_client_base_template()
    ctx = get_global_context()
    container = base.html_doc.find(lambda n:n.attr_manager.get_attr('data_ssdom_id') =="root-container")
    if container:
        container.add(LoginForm())
    return base

def SignupPage():
    base = get_client_base_template()
    ctx = get_global_context()
    container = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if container:
        container.add(SignupForm())
    return base