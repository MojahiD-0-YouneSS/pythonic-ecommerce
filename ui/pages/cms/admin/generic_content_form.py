from ui.components.shared import AdminForm
from ui.pages.base import get_management_base_template
from probo import DIV

def AdminGenericFormPage(title='Add New Item'):
    base = get_management_base_template()
    
    base_title = base.html_doc.find(lambda n:n.tag == 'TITLE')
    if base_title:
        base_title.inner_html(title)
    
    base_bode = base.html_doc.find(lambda n:n.attr_manager.get_attr('data_ssdom_id') == 'root-container')
    if base_bode:
        base_bode.add(DIV(AdminForm(), Class='p-5'))
    return base
