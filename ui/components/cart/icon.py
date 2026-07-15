from probo import A, I, SPAN


def cart_icon():
    return A(
        I(Class="bi bi-cart3"),
        SPAN(
            {'cart_item_count'},
            Class="badge rounded-pill bg-danger ms-1",
        ),
        href="/cart/",
        hx_swap_oob={'hx_oob', lambda **dvars:"true" if dvars.get('hx_oob', False) else False},
        Class="nav-link position-relative",
        Id="cart-icon",
        data_ssdom_id="cart-icon",
    )
