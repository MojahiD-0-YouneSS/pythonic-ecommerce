from django_abstract.base.base_operator import BaseOperator
from django_abstract.registry import register_operator


@register_operator()
class SessionOperator(BaseOperator):
    app_name = "client"
    domain = 'session'
    def __init__(self, session_key=None, domain=None, entry=None):
        super().__init__(session_key, domain, entry)
        self.validator = self.SessionValidator

    class SessionValidator(BaseOperator.BaseOperatorValidator):

        def meta_hook(self):
            pass


@register_operator()
class ClientOperator(BaseOperator):
    """
    The Security Bouncer for frontend users.
    Reads the Entry metadata and blocks unauthorized service calls.
    """
    app_name = 'client'
    domain = 'client'
    # Whitelist: What apps/services is the frontend allowed to touch?
    allowed_services = [
        "cart_model_service",
        "checkout_model_service",
        "user_model_service",
        "client_profile_model_service",
        "auth_service",
        "cms_model_service",  # Allowed to READ only
    ]

    def __init__(self, session_key=None, domain=None, entry=None):
        super().__init__(session_key, domain, entry)
        self.validator = self.ClientValidator

    class ClientValidator(BaseOperator.BaseOperatorValidator):

        def meta_hook(self):
            pass
