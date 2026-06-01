from probo import DIV, SPAN, I

def CheckoutError(error_message):
    """Fallback UI if validation fails."""
    return DIV(
        I(Class="bi bi-exclamation-triangle-fill text-danger me-2"),
        SPAN(error_message),
        Class="alert alert-danger rounded-3 shadow-sm mt-3",
    )
