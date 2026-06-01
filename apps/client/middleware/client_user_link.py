

class ClientUserBinderMiddleware:
    """
    Session filtering and Entry binding middleware.
    Ensures every request has a valid session and a fully hydrated framework Entry.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from apps.client.models import Client
        # 1. Ensure the user has a client object linked to it exists and is active
        if request.user.is_authenticated:
            # The Fix: Use update_or_create so the session_key stays synced on login!
            Client.objects.update_or_create(
                user=request.user,  # ONLY search by this unique field
                defaults={          # If found, update these. If not found, create with these.
                    'nickname': f"{request.user.first_name}_{request.user.last_name}_{request.user.username}",
                    'session_key': request.session.session_key
                }
            )
        response = self.get_response(request)
        return response
