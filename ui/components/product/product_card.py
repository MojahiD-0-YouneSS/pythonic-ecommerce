from probo import DIV, H5, P, IMG, BUTTON, A
from django.urls import reverse


def ProductCard():
    """Declarative component that pulls 'product' from the data pipeline."""
    return DIV(
        DIV(
            # Product Image (Using your static files)
            DIV(
                A(
                    IMG(
                        src={'image_url'},
                        Class="card-img-top",
                        alt="product image",
                    ),
                    # Product Details
                    DIV(
                        H5(
                            {'product.name'},
                            Class="card-title fw-bolder text-center",
                        ),
                        DIV(
                            {'product.base_price', lambda **dvars: f"${dvars.get('product.base_price')}"},
                            Class="text-center mb-3",
                        ),
                        Class="card-body p-4",
                    ),
                    href={'product.id', lambda **dvars: reverse(
                        "product:product-detail",
                        kwargs={"product_id": dvars.get("product.id")},
                    )},
                    Class='nav-link',
                )
            ),
            # HTMX Add to Cart Action
            DIV(
                DIV(
                    BUTTON(
                        "Add to cart",
                        hx_get={'product.id', lambda **dvars: reverse(
                            "cart:add_to_cart",
                            kwargs={"product_id": dvars.get("product.id")}
                        )},
                        hx_target="#messages-container",  # Updates your cart dynamically
                        hx_swap="innerHTML",
                        Class="btn btn-outline-dark mt-auto w-100",
                        Type="button",
                    ),
                    Class="text-center",
                ),
                Class="card-footer p-4 pt-0 border-top-0 bg-transparent",
            ),
            Class="card h-100 shadow-sm border-0",
        ),
        Class="col mb-5",
    )
    # return DIV(
    #     DIV(
    #         # Product Image (Using your static files)
    #         IMG(src="product_data.get('image_url', '/static/images/img/products/f1.jpg')", Class="card-img-top", alt=product_data.get('name')),

    #         # Product Details
    #         DIV(
    #             H5(product_data.get('name', 'Sample Product'), Class="card-title fw-bolder text-center"),
    #             DIV(f"${product_data.get('price', '0.00')}", Class="text-center mb-3"),
    #             Class="card-body p-4"
    #         ),

    #         # HTMX Add to Cart Action
    #         DIV(
    #             DIV(
    #                 BUTTON("Add to cart",
    #                        hx_post=f"/cart/add/{product_data.get('id', 1)}/",
    #                        hx_target="#cart-container", # Updates your cart dynamically
    #                        Class="btn btn-outline-dark mt-auto w-100"),
    #                 Class="text-center"
    #             ),
    #             Class="card-footer p-4 pt-0 border-top-0 bg-transparent"
    #         ),
    #         Class="card h-100 shadow-sm border-0"
    #     ),
    #     Class="col mb-5"
    # )
