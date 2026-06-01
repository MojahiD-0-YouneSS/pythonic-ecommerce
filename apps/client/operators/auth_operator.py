from apps.client.dependencies import get_client_dependency
from django_abstract.base import BaseOperator
from django_abstract.registry import register_operator

client_dependency_manager = get_client_dependency()

@register_operator()
class AuthenticatedOperator(BaseOperator):
    dependency = get_client_dependency()
    app_name = 'client'
    allowed_services = ['auth_service',]
    domain = 'authentication'

    def __init__(self, session_key=None, domain=None, entry=None):
        super().__init__(session_key, domain, entry)
        self.validator = self.AuthValidator

    class AuthValidator(BaseOperator.BaseOperatorValidator):

        def meta_hook(self):
            pass
