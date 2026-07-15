# ui/pages/cart_page.py
from probo import DIV
from ui.pages.base import get_client_base_template
from ui.components.cart.cart_item import CartItemTable
from ui.components.cart.cart_summary import CartSummaryCard
from ui.components.cart.client.discount_code import DiscountCode
from probo.type_hints import GenericSSDOM

def CartPage()-> GenericSSDOM:
        base = get_client_base_template()
        # 1. Update Title
        base_title = base.html_doc.find(lambda n: n.tag == 'TITLE')
        if base_title:
            base_title.inner_html({'title'})

        # 2. Build the main layout grid (Left: Items, Right: Summary)
        main_content = DIV(
            CartItemTable().add(CartSummaryCard()),
            DIV(Id='checkou-modal'),
            DiscountCode(),
        )

        # 3. Inject into the Base Layout
        base_body = base.html_doc.find(lambda n: n.attr_manager.get_attr("data_ssdom_id") == 'root-container')
        if base_body:
            base_body.inner_html(main_content)

        return base
