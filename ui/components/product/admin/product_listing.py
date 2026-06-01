from probo import DIV, H2, A
from django.urls import reverse

def AdminProductList(products, *args, **kwargs):
    product_items = []
    for product in products:
        item = DIV(
            H2(product.name),
            DIV(
                A(
                    "Edit",
                    href=reverse(
                        "product:admin-product-edit", kwargs={"product_id": product.id}
                    ),
                    Class="nav-link",
                ),
                Class="me-2 btn btn-primary btn-sm",
            ),
            DIV(
                A(
                    "View",
                    href=reverse(
                        "product:admin-product-detail",
                        kwargs={"product_id": product.id},
                    ),
                    Class="nav-link",
                ),
                Class="me-2 btn btn-outline-secondary btn-sm",
            ),
            Class="border p-3 mb-3 rounded col-md-4",
        )
        product_items.append(item)

    return DIV(DIV(*product_items,Class="row"), Class="admin-product-list")
