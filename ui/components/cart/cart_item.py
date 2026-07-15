from probo import (
    DIV,
    IMG,
    H6,
    P,
    SPAN,
    BUTTON,
    TABLE,
    THEAD,
    TR,
    TBODY,
    A,
    I,
    FORM,
    INPUT,
    LABEL,
)
from probo.components import frag, Frag
from probo.components.light_tags import (
    Ltd,
    Lth,
    Ltr,
)
from apps.product.dependencies import get_product_app_dependency
from apps.cart.dependencies import CartAppDependency
from apps.global_context import get_global_context
from ui.components.cart.cart_summary import CartSummaryCard
from ui.components.crf_token import CsrfToken

from django.urls import reverse


def CartItemRow() -> TR:
    """
    Renders a single row for a cart item using data_pipeline variables.
    """
    row_content = [
        Ltd(
            DIV(
                IMG(
                    src={'item.product_variant.image.url'},
                    Class="img-fluid rounded",
                    style="width: 50px;",
                ),
                SPAN({'item.product_variant.product.name'}, Class="ms-3 fw-bold"),
                Class="d-flex align-items-center",
            )
        ),
        Ltd({'item.product_variant.base_price'}, Class="align-middle"),
        Ltd(
            {'edit', 'post', 'item', 'qty_form', lambda **dvars :(
                SPAN(getattr(dvars.get('item'),'quantity', 0),Id='quantity', Class="fw-semibold")
                if dvars.get('edit',False) and dvars.get('post',False) or not dvars.get('edit',False)
                else (
                    FORM(
                        CsrfToken(),
                        DIV(
                            DIV(dvars.get('qty_form'), Class="col-7"),
                            DIV(
                                BUTTON(
                                    "Save",
                                    Type="submit",
                                    Class="btn btn-xs btn-success align-middle w-100",
                                ),
                                Class="col-5 ps-1",
                            ),
                            Class="row g-0 align-items-center",
                        ),
                        hx_post='#' if not dvars.get('item') else reverse(
                            "cart:edit-cart-item",
                            kwargs={"item_id":getattr(dvars.get('item'),'id','')},
                        ),
                        # We target ONLY this cell and swap its inner HTML with the view's raw response
                        hx_target=f"#qty-row-{(getattr(dvars.get('item'),'id',''))}",
                        hx_swap="innerHTML",
                        Class="m-0 p-1 border-0 bg-transparent",
                    )
                )
                    )},
            Class="align-middle",
            Id={'item', lambda **dvars: f"qty-row-{(getattr(dvars.get('item'),'id',''))}"},  # Matches the hx-target ID
        ),
        Ltd(
            # 1. Edit / Update Button
            BUTTON(
                I(Class="bi bi-pencil-square me-1"),
                "Edit",
                Class="btn btn-xs btn-outline-primary me-2 align-middle",
                # Passes item ID as a clean query parameter
                hx_get={'item', lambda **dvars:'#' if not dvars.get('item') else reverse( "cart:edit-cart-item", kwargs={"item_id": getattr(dvars.get('item'),'id','')})},
                # Swaps the edit form directly into your sidebar, modal, or form area
                hx_target={'item', lambda **dvars: f"#row-{(getattr(dvars.get('item'),'id',''))}"},
                hx_swap="outerHTML",
            ),
            # 2. Remove Button
            BUTTON(
                I(Class="bi bi-trash-fill me-1"),
                "Remove",
                Class="btn btn-xs btn-outline-danger align-middle",
                # Passes item ID as a clean query parameter
                hx_get={'item', lambda **dvars:'#' if not dvars.get('item') else reverse("cart:remove_from_cart", kwargs={"item_id": getattr(dvars.get('item'),'id','') })},
                # Automatically targets the corresponding table row to remove it from the DOM
                hx_target={'item', lambda **dvars: f"#row-{(getattr(dvars.get('item'),'id',''))}"},
                hx_swap="outerHTML",
                # Native browser confirmation dialog safely managed by HTMX
                hx_confirm="Are you sure you want to permanently delete this item?",
            ),
            Class="align-middle",
        ),
    ]

    # Unified Order Summary Column (Only added to the first row)
    # if is_first:
    #     row_content.append(
    #         Ltd(
    #             DIV(
    #                 H6("Order Summary", Class="fw-bold"),
    #                 P(f"Total Items: {total_items}", Class="small mb-1"),
    #                 P("Shipping: Free", Class="small mb-3"),
    #                 # A("Checkout",href="checkout/", Class="btn btn-primary btn-sm w-100"),

    #              Class="p-3 bg-light border rounded"),
    #             rowspan=str(total_items),
    #             Class="align-top"
    #         )
    #     )

    return TR(
            *row_content,
            Id={'item', lambda **dvars:f"row-{(getattr(dvars.get('item'), 'id', ''))}"},
            )

def CartItemTable() -> DIV:
    """
    Renders the full cart table or a placeholder if empty.
    """

    header = THEAD(
        Ltr(
            Lth("Product", scope="col"),
            Lth("Price", scope="col"),
            Lth("Qty", scope="col"),
            Lth(
                "Action",
                scope="col",
            ),
            # Lth("Summary", scope="col", style="width: 250px;"),
        )
    )
    def process_items(**kwargs):
        items = kwargs.get('cart_items',[])
        # edit = kwargs.get('edit',False)
        if not items:
            return DIV(
                P("Your cart is feeling a bit light...", Class="text-muted"),
                A("Go Shopping!", href="/", Class="btn btn-outline-secondary mb-3"),
                Class="text-center py-5 mb-3",
                Id='items-table',
                hx_swap_oob={'hx_oob'}
            )

        # Table Body
        rows = []
        for item in items:
            row = Frag(CartItemRow(), data_pipeline={'item':item,})
            rows.append(row)
        return frag(*rows)
    return DIV(
        TABLE(
            header,
            TBODY(
                {'cart_items','edit',process_items},
            ),
            Class="table table-hover align-middle border-top",
        ),
        Class="table-responsive",
        Id='items-table',
        hx_swap_oob={'hx_oob'}
    )
