from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, SECTION, HR

def get_status_badge(status) -> str:
    """Returns a Bootstrap badge based on order status."""
    status_map = {
        'Pending': 'warning text-dark',
        'Processing': 'primary',
        'Shipped': 'info text-white',
        'Delivered': 'success',
        'Canceled': 'danger',
        'Returned': 'secondary',
    }
    color = status_map.get(status, 'secondary')
    return color

def get_payment_badge(status) -> str:
    """Returns a badge for payment status."""
    color = 'success' if status == 'Paid' else 'danger' if status == 'Unpaid' else 'warning text-dark'
    return color
