from probo import INPUT
from apps.global_context import get_global_context
def CsrfToken() -> INPUT:
    """
    Renders the hidden CSRF input field required by Django for POST forms.
    """
    context = get_global_context()    
    return INPUT(
        type="hidden",
        name="csrfmiddlewaretoken",
        value=context.get('csrf_token')
    )