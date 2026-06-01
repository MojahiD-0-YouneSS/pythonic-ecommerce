from django_abstract.base.base_model_service import BaseModelService
from django_abstract.registry import (
    service_settings,
    ServiceSettings,
    action_method_fields,
)
from apps.cms.dependencies import CmsAppDependency
from django.utils import timezone


class QuoteModelService(BaseModelService):
    hooks_list = []
    model_dependency = CmsAppDependency()
    service_slug = "quote_model_service"
    model_slug = "quote"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.QuoteServiceValidator
        self.init_state_hook()

    class QuoteServiceValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.proxy_register()

        def proxy_register(self):
            self.regester_method("update_status", self.update_status)
            self.regester_method("propose_new_price", self.propose_new_price)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["id"],
                VALID_FIELDS_PER_ACTION={
                    "update_status": ["status"],
                    "propose_new_price": ["proposed_price"],
                },
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("status")
        def update_status(self, status):
            quote = self.parent_service.db_record
            valid_statuses = ["pending", "approved", "rejected", "expired"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

            quote.status = status
            quote.save()
            return {"status_updated": True, "new_status": quote.status}

        @action_method_fields("proposed_price")
        def propose_new_price(self, proposed_price):
            quote = self.parent_service.db_record
            quote.proposed_price = proposed_price
            quote.status = "pending"  # Reset status for client review
            quote.save()
            return {"price_updated": True, "new_price": str(quote.proposed_price)}


class BannerModelService(BaseModelService):
    hooks_list = []
    model_dependency = CmsAppDependency()
    service_slug = "banner_model_service"
    model_slug = "banner"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.BannerServiceValidator
        self.init_state_hook()

    class BannerServiceValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.proxy_register()

        def proxy_register(self):
            self.regester_method("toggle_featured", self.toggle_featured)
            self.regester_method("update_schedule", self.update_schedule)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["id"],
                VALID_FIELDS_PER_ACTION={
                    "toggle_featured": ["is_featured"],
                    "update_schedule": ["start_date", "end_date"],
                },
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("is_featured")
        def toggle_featured(self, is_featured):
            banner = self.parent_service.db_record
            banner.is_featured = bool(is_featured)
            banner.save()
            return {"featured_toggled": True, "is_featured": banner.is_featured}

        @action_method_fields("start_date", "end_date")
        def update_schedule(self, start_date, end_date):
            banner = self.parent_service.db_record
            banner.start_date = start_date
            banner.end_date = end_date
            banner.save()
            return {"schedule_updated": True}


class TestimonyModelService(BaseModelService):
    hooks_list = []
    model_dependency = CmsAppDependency()
    service_slug = "testimony_model_service"
    model_slug = "testimony"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.TestimonyServiceValidator
        self.init_state_hook()

    class TestimonyServiceValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.proxy_register()

        def proxy_register(self):
            self.regester_method("approve_testimony", self.approve_testimony)
            self.regester_method("toggle_highlight", self.toggle_highlight)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["id"],
                VALID_FIELDS_PER_ACTION={
                    "approve_testimony": ["is_approved"],
                    "toggle_highlight": ["highlighted"],
                },
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("is_approved")
        def approve_testimony(self, is_approved):
            testimony = self.parent_service.db_record
            testimony.is_approved = bool(is_approved)
            testimony.save()
            return {"approval_changed": True, "is_approved": testimony.is_approved}

        @action_method_fields("highlighted")
        def toggle_highlight(self, highlighted):
            testimony = self.parent_service.db_record
            testimony.highlighted = bool(highlighted)
            testimony.save()
            return {"highlight_toggled": True}


class ContactModelService(BaseModelService):
    hooks_list = []
    model_dependency = CmsAppDependency()
    service_slug = "contact_model_service"
    model_slug = "contact"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.ContactServiceValidator
        self.init_state_hook()

    class ContactServiceValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.proxy_register()

        def proxy_register(self):
            self.regester_method("mark_responded", self.mark_responded)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["id"],
                VALID_FIELDS_PER_ACTION={"mark_responded": ["response_message"]},
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("response_message")
        def mark_responded(self, response_message):
            contact = self.parent_service.db_record
            if contact.responded:
                raise ValueError("Contact inquiry has already been responded to.")

            contact.mark_as_responded(response_message=response_message)
            return {"marked_responded": True, "response_date": contact.response_date}


class PosterModelService(BaseModelService):
    hooks_list = []
    model_dependency = CmsAppDependency()
    service_slug = "poster_model_service"
    model_slug = "poster"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.PosterServiceValidator
        self.init_state_hook()

    class PosterServiceValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.regester_method("mark_responded", self.mark_responded)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["id"],
                VALID_FIELDS_PER_ACTION={"mark_responded": ["response_message"]},
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("response_message")
        def mark_responded(self, response_message):
            contact = self.parent_service.db_record
            if contact.responded:
                raise ValueError("Contact inquiry has already been responded to.")

            contact.mark_as_responded(response_message=response_message)
            return {"marked_responded": True, "response_date": contact.response_date}
