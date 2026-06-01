from ui.components.cart.forms.discount_code import get_discout_form
from ui.pages.base import get_management_base_template
from probo import DIV

def admin_discout_page(*args,**kwargs):
    base = get_management_base_template()
    base_title = base.html_doc.find(lambda n:n.tag == "TITLE")
    
    if base_title:
        base_title.inner_html('Admin Panel | Discount operations')
    
    base_body = base.html_doc.find(lambda n:n.attr_manager.get_attr('data_ssdom_id') =='root-container')
    if base_body:
        base_body.add(
            DIV(
                get_discout_form(*args,**kwargs),
                Class='m-5',
                Id='admin-form-container'
            )
        )
    return base
    


