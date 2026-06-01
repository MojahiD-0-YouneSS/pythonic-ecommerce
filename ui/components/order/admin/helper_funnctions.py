from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, SECTION, HR

def get_status_badge(status):
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
    return SPAN(status, Class=f"badge bg-{color} small fw-semibold")

def get_payment_badge(status):
    """Returns a badge for payment status."""
    color = 'success' if status == 'Paid' else 'danger' if status == 'Unpaid' else 'warning text-dark'
    return SPAN(status, Class=f"badge rounded-pill bg-{color} px-2", style="font-size: 0.7rem;")
