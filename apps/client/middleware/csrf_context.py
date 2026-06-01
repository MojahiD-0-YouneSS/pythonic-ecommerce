from django.middleware.csrf import get_token
from apps.global_context import get_global_context


class CsrfContextMiddleware:
    """
    Automatically populates the global Probo Context with Django's CSRF token
    on every incoming HTTP request. Bypasses the need for manual view-based hydration.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Force the generation and retrieval of the active CSRF token.
        # This automatically sets the 'csrftoken' cookie in the user's browser
        # and grabs the token string securely.
        csrf_token = get_token(request)

        # 2. Fetch our global Probo Context singleton
        context = get_global_context()

        # 3. Securely inject the token into the global UI state
        context.put("csrf_token", csrf_token)

        # 4. Continue the Django request/response pipeline
        response = self.get_response(request)
        return response
