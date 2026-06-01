from probo import DIV, H2, H4, IMG, P, I, BUTTON, INPUT
from apps.global_context import get_global_context
from django.urls import reverse
from ui.components.crf_token import CsrfToken
def ProductDetail(product=None):
    Context = get_global_context()  # Get global context for things like user info, cart count, etc.

    """Single Product Detail Page with Add to Cart HTMX logic."""
    product = product or Context.get("product_detail")
    is_out_of_stock = product["stock"] == 0
    if not product:
        return DIV(
            H2("Product Not Found", Class="text-center text-danger my-5"),
            Class="container py-5"
        )
    return DIV(
        DIV(
            # Left Column: Big Image
            DIV(
                IMG(
                    src=product["image_url"],
                    Class="img-fluid rounded shadow",
                    alt=product["name"],
                ),
                Class="col-md-6 mb-4 mb-md-0",
            ),
            # Right Column: Details & Actions
            DIV(
                H2(product["name"], Class="fw-bold mb-2"),
                H4(f"${product['base_price']}", Class="text-primary mb-3"),
                P(
                    product["description"],
                    Class="text-muted mb-4",
                    style="line-height: 1.7;",
                ),
                # Features List
                DIV(
                    *[
                        P(
                            I(Class="bi bi-check2 text-success me-2"),
                            feat,
                            Class="small text-muted mb-1",
                        )
                        for feat in product["features"]
                    ],
                    Class="mb-4",
                ),
                # Stock Status
                P(
                    I(
                        Class=(
                            "bi bi-circle-fill text-success me-2 smaller"
                            if not is_out_of_stock
                            else "bi bi-circle-fill text-danger me-2 smaller"
                        )
                    ),
                    (
                        f"{product['stock']} in stock"
                        if not is_out_of_stock
                        else "Out of Stock"
                    ),
                    Class=f"small fw-bold {'text-success' if not is_out_of_stock else 'text-danger'} mb-4",
                ),
                # Interactive Cart Box
                DIV(
                    # Quantity Selector
                    DIV(
                        BUTTON(
                            "-",
                            Class="btn btn-outline-secondary",
                            type="button",
                            onclick="document.getElementById('qty').value > 1 ? document.getElementById('qty').value-- : null",
                        ),
                        INPUT(
                            type="number",
                            id="qty",
                            name="quantity",
                            value="1",
                            min="1",
                            max=str(product["stock"]),
                            Class="form-control text-center fw-bold",
                            style="max-width: 65px;",
                        ),
                        BUTTON(
                            "+",
                            Class="btn btn-outline-secondary",
                            type="button",
                            onclick=f"document.getElementById('qty').value < {product['stock']} ? document.getElementById('qty').value++ : null",
                        ),
                        Class="input-group input-group-lg me-3",
                        style="width: 150px;",
                    ),
                    # HTMX Add to Cart Button
                    BUTTON(
                        I(Class="bi bi-cart-plus me-2"),
                        "Add to Cart",
                        Class="btn btn-dark btn-lg flex-grow-1 fw-bold shadow-sm",
                        disabled=is_out_of_stock,
                        hx_get=reverse(
                            "cart:add_to_cart", kwargs={"product_id": product["id"]}
                        ),
                        hx_include="[name='quantity']",  # Tells HTMX to grab the qty input value
                        onclick='document.getElementById("qty").value=1',
                        hx_target='#messages-container',
                        hx_swap='innerHTML'
                    ),
                    Class="d-flex align-items-center bg-light p-4 rounded-3 border",
                ),
                Class="col-md-6 ps-md-5 d-flex flex-column justify-content-center",
            ),
            Class="row container mx-auto my-5",
        )
    )
