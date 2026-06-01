from apps.client.systems.session_ecosystem.session_filter import SessionFilterSystem


class EntryMiddleware:
    """
    Session filtering and Entry binding middleware.
    Ensures every request has a valid session and a fully hydrated framework Entry.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Ensure the session exists and is active
        if not request.session.session_key:
            request.session.create()

        # 2. Extract context and hydrate the Master Entry
        extractor = SessionFilterSystem(request)

        _, entry = extractor.execute()

        # 3. Bind the hydrated entry to the request object
        # so Systems can access it without repeating the extraction
        request.django_abstract_entry = entry

        # 4. Continue the Django request/response cycle
        response = self.get_response(request)
        return response
