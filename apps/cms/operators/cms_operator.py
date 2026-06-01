from django_abstract.base.base_operator import BaseOperator
from django_abstract.registry import register_operator


@register_operator()
class CmsOperator(BaseOperator):
    """
    Security gateway for Content Management.
    Enforces strict read-only rules for guests and clients,
    while allowing full CRUD for staff/admins.
    """

    allowed_services = [
        "quote_model_service",
        "banner_model_service",
        "testimony_model_service",
        "contact_model_service",
        "homepage_editor_model_service",
        "poster_model_service",
    ]
    def __init__(self, session_key=None,):
        super().__init__(session_key=session_key, domain='cms')
