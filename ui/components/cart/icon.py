from probo import A, I, SPAN


def cart_icon(cart_count,hx_oob=False):
    return A(
        I(Class="bi bi-cart3"),
        SPAN(
            cart_count or 0,
            Class="badge rounded-pill bg-danger ms-1",
        ),
        href="/cart/",
        hx_swap_oob="true" if hx_oob else False,
        Class="nav-link position-relative",
        Id="cart-icon",
        data_ssdom_id="cart-icon",
    )
