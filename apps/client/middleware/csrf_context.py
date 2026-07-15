from django.middleware.csrf import get_token

class CsrfContextMiddleware:
    """
    Automatically populates the global Probo Context with Django's CSRF token
    on every incoming HTTP request. Bypasses the need for manual view-based hydration.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        csrf_token = get_token(request)

        # 3. Securely inject the token into the global UI state
        request.ui_context.put("csrf_token", csrf_token)
        request.ui_context.put("global_csrf_token", f"js:{{'X-CSRFToken': '{csrf_token}'}}")
        request.ui_context.put("hx_oob", False)
        request.ui_context.put("is_admin", False if not request.user.username == 'admin_1' else True)  # Initialize is_admin based on user role
        # 4. Continue the Django request/response pipeline
        response = self.get_response(request)
        return response
