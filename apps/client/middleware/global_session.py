from apps.global_context import get_global_context


class GlobalSessionMiddleware:
    """
    Ensures every request has a valid session key and injects it
    into the application's global context for use by DJA Services.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Force session creation if it doesn't exist
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        # 2. Inject into the Global Context
        # Note: If your global context is a true Singleton, be careful with
        # concurrent requests in production overriding this.
        # For a portfolio demo/local dev, this is perfectly fine.
        global_ctx = get_global_context()
        global_ctx.put("session_key", session_key)
        global_ctx.put("user_auth", request.user.is_authenticated)

        # Optionally, you can attach it directly to the request object
        # if your services prefer extracting it from there.
        # request.dja_session_key = session_key

        # 3. Continue processing the request
        response = self.get_response(request)

        return response
