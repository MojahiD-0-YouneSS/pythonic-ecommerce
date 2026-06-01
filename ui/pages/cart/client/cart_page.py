# ui/pages/cart_page.py
from probo import DIV
from ui.components.cart.cart_item import CartItemTable
from ui.components.cart.cart_summary import CartSummaryCard
from ui.components.cart.client.discount_code import DiscountCode
from ui.pages.base import get_client_base_template

class CartPage:

    def __init__(
        self,
        cart,
        items, title="Your Shopping Cart",
    ):
        self._title = title
        self.cart = cart
        self.items = items

    def render(self):
        base = get_client_base_template()

        # 1. Update Title
        base_title = base.html_doc.find(lambda n: n.tag == 'TITLE')
        if base_title:
            base_title.inner_html(self._title)

        # 2. Build the main layout grid (Left: Items, Right: Summary)
        main_content = DIV(
            CartItemTable(self.items).add(CartSummaryCard(self.cart)),
            DIV(Id='checkou-modal'),
            DiscountCode(),
        )

        # 3. Inject into the Base Layout
        base_body = base.html_doc.find(lambda n: n.attr_manager.get_attr("data_ssdom_id") == 'root-container')
        if base_body:
            base_body.inner_html(main_content)

        return base.render()
