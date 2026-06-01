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


def CartItemRow(item, edit=False,post=False) -> Ltr|TR:
    """
    Renders a single row for a cart item.
    If it's the first row, it includes the unified Order Summary column.
    """
    ctx = get_global_context()
    qty_form = ctx.get("qty_form_html")
    # name = item.product.name
    image = (
        get_product_app_dependency()
        .select_product_image.model_class.objects.filter(variant=item.product_variant)
        .first()
        .image
    )
    # item=CartAppDependency().select_cart_item.access_db.get(cart=ctx.get('cart'),product_variant=item,is_active=True)
    # item = model_to_dict(item)
    # item["image"] = image
    # item["name"] = name
    # Item Details Column
    row_content = [
        Ltd(
            DIV(
                IMG(
                    src=image,
                    Class="img-fluid rounded",
                    style="width: 50px;",
                ),
                SPAN(item.product_variant.product.name, Class="ms-3 fw-bold"),
                Class="d-flex align-items-center",
            )
        ),
        Ltd(f"${item.product_variant.base_price}", Class="align-middle"),
        Ltd(
            (
                SPAN(str(item.quantity), Class="fw-semibold")
                if edit and post or not edit
                else (
                    FORM(
                        CsrfToken(),
                        DIV(
                            DIV(qty_form, Class="col-7"),
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
                        hx_post=reverse(
                            "cart:edit-cart-item",
                            kwargs={"item_id": item.id},
                        ),
                        # We target ONLY this cell and swap its inner HTML with the view's raw response
                        hx_target=f"#qty-row-{item.id}",
                        hx_swap="innerHTML",
                        Class="m-0 p-1 border-0 bg-transparent",
                    )
                )
            ),
            Class="align-middle",
            Id=f"qty-row-{item.id}",  # Matches the hx-target ID
        ),
        Ltd(
            # 1. Edit / Update Button
            BUTTON(
                I(Class="bi bi-pencil-square me-1"),
                "Edit",
                Class="btn btn-xs btn-outline-primary me-2 align-middle",
                # Passes item ID as a clean query parameter
                hx_get=reverse("cart:edit-cart-item", kwargs={"item_id": item.id}),
                # Swaps the edit form directly into your sidebar, modal, or form area
                hx_target=f"#row-{item.id}",
                hx_swap="outerHTML",
            ),
            # 2. Remove Button
            BUTTON(
                I(Class="bi bi-trash-fill me-1"),
                "Remove",
                Class="btn btn-xs btn-outline-danger align-middle",
                # Passes item ID as a clean query parameter
                hx_get=reverse("cart:remove_from_cart", kwargs={"item_id": item.id}),
                # Automatically targets the corresponding table row to remove it from the DOM
                hx_target=f"#row-{item.id}",
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

    return (
        Ltr(
            *row_content,
            Id=f"row-{item.id}",
        )
        if not edit
        else TR(
            *row_content,
            Id=f"row-{item.id}",
        )
    )


def CartItemTable(items,hx_oob=False) -> DIV:
    """
    Renders the full cart table or a placeholder if empty.
    """
    if not items:
        return DIV(
            P("Your cart is feeling a bit light...", Class="text-muted"),
            A("Go Shopping!", href="/", Class="btn btn-outline-secondary mb-3"),
            Class="text-center py-5 mb-3",
            Id='items-table',
            hx_swap_oob='true' if hx_oob else False
        )

    # Table Header
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

    # Table Body
    rows = []
    for item in items.all():
        rows.append(
            CartItemRow(
                item,
            )
        )

    return DIV(
        TABLE(
            header,
            TBODY(
                *rows,
            ),
            Class="table table-hover align-middle border-top",
        ),
        Class="table-responsive",
        Id='items-table',
        hx_swap_oob='true' if hx_oob else False
    )
