from django_abstract.base.base_model_service import BaseModelService
from apps.client.dependencies import ClientAppDependency
from django_abstract.registry import service_settings, action_method_fields, ServiceSettings, register_service

@register_service()
class ClientModelService(BaseModelService):
    hooks_list = []
    model_dependency = ClientAppDependency()
    service_slug = "client_model_service"
    model_slug = "client"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.ClientServiceValidator
        self.init_state_hook()

    class ClientServiceValidator(BaseModelService.BaseServiceValidator):

        def meta_hook(self):
            self.regester_method("change_password", self.change_password)
            self.regester_method("deactivate_account", self.deactivate_account)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["id"],
                VALID_FIELDS_PER_ACTION={
                    "change_password": ["old_password", "new_password"],
                    "deactivate_account": ["reason"],
                },
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("old_password", "new_password")
        def change_password(self, old_password, new_password):
            client = self.parent_service.db_record
            if not client:
                raise ValueError("Client record not found.")

            # Assuming Django's AbstractBaseUser or similar is used
            if not client.check_password(old_password):
                raise ValueError("Invalid old password.")

            client.set_password(new_password)
            client.save()
            return {"password_changed": True}

        @action_method_fields("reason")
        def deactivate_account(self, reason):
            client = self.parent_service.db_record
            client.is_active = False
            client.save()
            return {"account_deactivated": True, "reason_logged": reason}


@register_service()
class ClientProfileModelService(BaseModelService):
    hooks_list = []
    model_dependency = ClientAppDependency()
    service_slug = "client_profile_model_service"
    model_slug = "client_profile"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.ClientProfileServiceValidator
        self.init_state_hook()

    class ClientProfileServiceValidator(BaseModelService.BaseServiceValidator):

        def meta_hook(self):
            self.regester_method("update_info", self.update_info)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["client_id"],
                VALID_FIELDS_PER_ACTION={
                    "update_info": ["first_name", "last_name", "phone_number"]
                },
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("first_name", "last_name", "phone_number")
        def update_info(self, first_name, last_name, phone_number):
            profile = self.parent_service.db_record
            if not profile:
                raise ValueError("Profile record not found.")

            profile.first_name = first_name
            profile.last_name = last_name
            
            profile.user.first_name = first_name
            profile.user.last_name = last_name
            
            profile.phone_number = phone_number
            profile.save()

            order_history  = None
            shipping_address  = None
            billing_address  = None
            

            return {"profile_updated": True, "phone": profile.phone_number}


@register_service()
class ShoppingHistoryModelService(BaseModelService):
    hooks_list = []
    model_dependency = ClientAppDependency()
    service_slug = "shopping_history_model_service"
    model_slug = "shopping_history"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.ShoppingHistoryServiceValidator
        self.init_state_hook()

    class ShoppingHistoryServiceValidator(BaseModelService.BaseServiceValidator):

        def meta_hook(self):
            self.regester_method("log_purchase", self.log_purchase)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["client_id"],
                VALID_FIELDS_PER_ACTION={
                    "log_purchase": ["client_id", "order_id", "total_amount", "status"]
                },
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("client_id", "order_id", "total_amount", "status")
        def log_purchase(self, client_id, order_id, total_amount, status):
            # Using the framework creator to append a new history record
            history_record = self.dependency.create_shopping_history.access_db.create(
                client_id=client_id,
                order_id=order_id,
                total_amount=total_amount,
                status=status,
            )
            self.behavior.service_data.update({"purchase_logged": True, "history_id": history_record.id})

@register_service()
class GuestIdentityModelService(BaseModelService):
    hooks_list = []
    model_dependency = ClientAppDependency()
    service_slug = "guest_identity_model_service"
    model_slug = "guest_identity"

    def __init__(self, session_key, *args, **db_required_fields):
        super().__init__(session_key=session_key, *args, **db_required_fields)
        self.validator = self.GuestIdentityServiceValidator
        self.init_state_hook()

    class GuestIdentityServiceValidator(BaseModelService.BaseServiceValidator):

        def meta_hook(self):
            self.regester_method("track_visit", self.track_visit)
            self.regester_method("convert_to_client", self.convert_to_client)

        @service_settings(
            settings=ServiceSettings(
                MINIMUM_READ_FIELDS=["session_key"],
                VALID_FIELDS_PER_ACTION={
                    "track_visit": ["ip_address", "user_agent"],
                    "convert_to_client": ["client_id"],
                },
            )
        )
        def load_settings(self, settings):
            return super().load_settings(settings)

        @action_method_fields("ip_address", "user_agent")
        def track_visit(self, ip_address, user_agent):
            guest = self.parent_service.db_record
            if not guest:
                guest = self.parent_service.creator.create(
                    session_key=self.parent_service.session_key,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    visits=1,
                )
            else:
                guest.visits += 1
                guest.ip_address = ip_address  # Update to latest IP
                guest.save()

            return {"guest_tracked": True, "visits": guest.visits}

        @action_method_fields("client_id")
        def convert_to_client(self, client_id):
            guest = self.parent_service.db_record
            if not guest:
                raise ValueError("Guest identity not found for conversion.")

            guest.converted_to_client_id = client_id
            guest.is_converted = True
            guest.save()

            return {"converted": True, "client_id": client_id}

@register_service()
class UserModelService(BaseModelService):
    """
    Database logic layer for the User model.
    Encapsulates all database-bound creation and mutations.
    """

    model_dependency = ClientAppDependency()
    model_slug = "user"
    service_slug = "user_model_service"
    # hooks_list = ["auth_service",]

    def __init__(self, session_key=None, *args, **db_fields):
        super().__init__(
            session_key=session_key, *args, include_session=False, **db_fields
        )
        self.validator = self.UserValidator
        self.init_state_hook()

    class UserValidator(BaseModelService.BaseServiceValidator):
        def meta_hook(self):
            self.MINIMUM_READ_FIELDS = ["id"]
            self.MINIMUM_WRITE_FIELDS = ["username", "email", "password"]
            self.SERVICE_DOMAIN_FIELDS = [
                "pk",
                "username",
                "email",
                "password",
                "first_name",
                "last_name",
            ]

            self.VALID_FIELDS_PER_ACTION = {
                "create_user": [
                    "username",
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                ],
                "update_user": ["pk", "email", "first_name", "last_name"],
                "update_user_logins": ['pk', "password"],
            }
            self.regester_method("create_user", self.create_user)
            self.regester_method("update_user", self.update_user)
            self.regester_method("update_user_logins", self.update_user_logins)
            self.set_db_methods_fields('read_entry','pk')
            self.set_db_methods_fields('delete_entry','pk')
            self.set_db_methods_fields(
                "create_entry", self.get_method_args("create_user",keys=True)
            )

        def create_user(self):
            """
            Performs the physical database write operation.
            Only called when the pure validation layers upstream approve.
            """
            username, email, password, first_name, last_name = self.get_method_args("create_user")

            try:
                user = self.dependency.create_user.access_db.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                self.behavior.service_data.update(
                    {
                        **user.__dict__,
                        "success": True,
                        "message": "Welcome! Registration completed successfully.",
                    }
                )
            except Exception as e:
                self.parent_service.entry.errors["service"] = (
                    f"Failed to register account: {str(e)}"
                )
                self.behavior.service_data.update({"success": False})

        def update_user(self,):
            pk, email, first_name, last_name = self.get_method_args("update_user")

            try:
                user = self.dependency.select_user.access_db.get(id=pk,)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                self.behavior.service_data.update(
                    {
                        **user.__dict__,
                        "success": True,
                        "message": "Welcome! Profile updates completed successfully.",
                    }
                )
            except Exception as e:
                self.parent_service.entry.errors["service"] = (
                    f"Failed to update profile: {str(e)}"
                )
                self.behavior.service_data.update({"success": False})

        def update_user_logins(self,):
            pk, password, = self.get_method_args(
                "update_user_logins"
            )

            try:
                user = self.dependency.select_user.access_db.get(id=pk)
                user.set_password(password)
                user.save()
                self.behavior.service_data.update(
                    {
                        **user.__dict__,
                        "success": True,
                        "message": "Login updates completed successfully.",
                    }
                )
            except Exception as e:
                self.parent_service.entry.errors["service"] = (
                    f"Failed to update login information: {str(e)}"
                )
                self.behavior.service_data.update({"success": False})
