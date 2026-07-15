from probo.templates import base_template_tree 
from probo import DIV, LINK, SCRIPT
from ui.components.cms.admin_panel import admin_panel
from ui.components.cms.client_panel import ClientHeader, ClientFooter
from apps.global_context import get_global_context

def get_base_template(*args,**kwargs):
    base = base_template_tree(override_body=True)
    base.html_doc.load_data(get_global_context())
    base.html_doc.get_data_pipeline.put('x',12345679)
    base_head = base.html_doc.find(lambda n:n.tag == 'HEAD')
    if base_head:
        base_head.add(
            LINK(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
            )
        ).add(
            SCRIPT(
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js",
                integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM",
                crossorigin="anonymous",
            )
        ).add(
            LINK(
                rel="stylesheet",
                href="/static/css/style.css"
            )
        ).add(
            LINK(
                rel="stylesheet",
                href="/static/css/premium.css"
            )
        )
    base_body = base.html_doc.find(lambda n:n.tag == 'BODY')
    if base_body:
        base_body.attributes['hx_headers']=base_body.get_data('global_csrf_token')

        # hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    return base

def get_management_base_template(*args,**kwargs):
    base = get_base_template()
    base_body = base.html_doc.find(lambda n:n.tag == 'BODY')
    if base_body:
        base_body.add(
            DIV(
                Id="messages-container",
                Class="toast-container position-fixed bottom-0 end-0 p-3",
                style="z-index: 1055;",
                data_ssdom_id="root-messages-container",
            )
        ).add(admin_panel())
    return base

def get_client_base_template(*args,**kwargs):
    from probo import A, LI
    from django.urls import reverse

    base = get_base_template()
    base_body = base.html_doc.find(lambda n:n.tag == 'BODY')
    
    if base_body:
        base_body.add(
            DIV(
                Id="messages-container",
                data_ssdom_id="root-messages-container",
                Class="toast-container position-fixed bottom-0 end-0 p-3",
                style="z-index: 1055;",
            )
        ).add(
            ClientHeader(),
        ).add(
            DIV(Class="container", data_ssdom_id="root-container"),
        ).add(
            ClientFooter(),
        )
    return base
