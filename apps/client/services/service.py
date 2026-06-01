from django.contrib.auth import authenticate, login, logout
from django_abstract.base.base_service import BaseService
from django_abstract.utilities import ServiceEntryData
from django_abstract.registry import register_service
from apps.client.dependencies import get_client_dependency
from apps.global_context import get_global_context

@register_service()
class AuthService(BaseService):
    """
    Pure logical service handling core authentication algorithms.
    Contains zero direct database write logic. delegates creation to UserModelService.
    """

    service_slug = "auth"
    hooks_list = ["user_model_service"]  # Registered hooks to invoke via hook_pad

    def __init__(self, session_key=None, *args, **kwargs):
        super().__init__(session_key=session_key, *args, **kwargs)
        self.validator = self.AuthServiceValidator

    class AuthServiceValidator(BaseService.BaseServiceValidator):

        def meta_hook(self):
            """
            Define validation criteria and exposed service methods.
            We require 'request' to execute stateful session mutations safely.
            """
            self.SERVICE_DOMAIN_FIELDS = [
                "username",
                "email",
                "password",
                "first_name",
                "last_name",
                "username_or_email",
                "request",
                "pk",
                "current_password",
                "new_password",
                "confirmed_password",
                
            ]
            self.VALID_FIELDS_PER_ACTION = {
                "register_user": [
                    "username",
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "request",
                    ],
                "login_user": ["username_or_email", "password", "request"],
                "logout_user": ["request"],
                "update_user_info": ["pk", "email", "first_name", "last_name"],
                "update_user_logins": [
                    "pk",
                    "current_password",
                    "new_password",
                    "confirmed_password",
                ],
            }

            self.regester_method("register_user", self.register_user)
            self.regester_method("login_user", self.login_user)
            self.regester_method("logout_user", self.logout_user)
            self.regester_method("update_user_info", self.update_user_info)
            self.regester_method("update_user_logins", self.update_user_logins)

        def register_user(self):
            """
            Handles safe, logical validation for user registration.
            If valid, passes the payload to UserModelService via hook_pad.
            """
            username, email, password, first_name, last_name = self.get_method_args(
                "register_user"
            )
            dpendency = get_client_dependency()
            # 1. Pure logical validation checks
            if dpendency.select_user.access_db.filter(username=username).exists():
                self.parent_service.entry.errors["username"] = (
                    "This username is already taken."
                )
                self.behavior.service_data.update({"success": False})
                return

            if dpendency.select_user.access_db.filter(email=email).exists():
                self.parent_service.entry.errors["email"] = (
                    "This email is already registered."
                )
                self.behavior.service_data.update({"success": False})
                return

            # 2. Package the payload to pass down the pipeline

            sed = ServiceEntryData(
                service_data=(
                    {
                        "method_name": "create_user",
                        "username": username,
                        "email": email,
                        "password": password,
                        "first_name": first_name,
                        "last_name": last_name,
                        "service_args": self.data.get("service_args"),
                    }
                )
            )
            # 3. Securely hand over DB creation to UserModelService via hook_pad
            success = self.parent_service.hook_pad("user_model_service", entry=sed)

            if success:
                # Merge the newly created user state back into the operator sequence
                self.behavior.service_data.update(
                    self.parent_service.entry.service_data
                )
            else:
                self.behavior.service_data.update({"success": False})

        def login_user(self):
            """
            Authenticates a client's credentials and logs them in using the passed request object.
            """
            username_or_email, password, request = self.get_method_args("login_user")
            dpendency = get_client_dependency()
            if not request:
                self.parent_service.entry.errors["system"] = (
                    "Missing active HTTP request context."
                )
                self.behavior.service_data.update({"success": False})
                return

            # Resolve username if email is passed
            username = username_or_email
            if "@" in username_or_email:
                try:
                    target_user = dpendency.select_user.access_db.get(
                        email=username_or_email
                    )
                    username = target_user.username
                except dpendency.select_user.model_class.DoesNotExist:
                    pass

            # Authenticate credentials securely
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    # Write to Django session cookies explicitly
                    login(request, user)
                    self.behavior.service_data.update(
                        {
                            "user": user,
                            "success": True,
                            "message": f"Successfully signed in! Welcome back, {user.username}.",
                        }
                    )
                else:
                    self.parent_service.entry.errors["auth"] = (
                        "This client account has been suspended."
                    )
                    self.behavior.service_data.update({"success": False})
            else:
                self.parent_service.entry.errors["auth"] = (
                    "Invalid credentials. Please verify your details."
                )
                self.behavior.service_data.update({"success": False})

        def logout_user(self):
            """
            Destroys user session explicitly.
            """
            request = self.get_method_args("logout_user")[0]
            if request:
                logout(request)
                self.behavior.service_data.update(
                    {"success": True, "message": "Logged out successfully."}
                )
            else:
                self.behavior.service_data.update({"success": False})

        def update_user_info(self,):
            pk, email, first_name, last_name = self.get_method_args("update_user_info")
            dpendency = get_client_dependency()
            # 1. Pure logical validation checks
            if (
                dpendency.select_user.access_db.exclude(id=pk)
                .filter(email=email)
                .exists()
            ):
                self.parent_service.entry.errors["email"] = (
                    "This email is already in use by another account."
                )
                self.behavior.service_data.update({"success": False})
                return False
            sed = ServiceEntryData(
                service_data=(
                    {
                        "method_name": "update_user",
                        "pk": pk,
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "service_args": {
                            "session_key": self.parent_service.session_key,
                            "load_record": False,
                        },
                    }
                )
            )

            # 3. Dispatch to Database
            success = self.parent_service.hook_pad("user_model_service", entry=sed)
            self.behavior.service_data.update({"success": success})
            return success

        def update_user_logins(self,):
            pk, current_password, new_password, confirmed_password = self.get_method_args(
                "update_user_logins"
            )
            dependency = get_client_dependency()
            # 1. Pure logical validation checks
            if (
                new_password != confirmed_password
            ):
                self.parent_service.entry.errors["password_mismatch"] = (
                    "The new password and confirmation do not match."
                )
                self.behavior.service_data.update({"success": False})
                return False
            if (
                dependency.select_user.access_db.exclude(id=pk)
                .filter(password=current_password)
                .exists()
            ):
                self.parent_service.entry.errors["current_password"] = (
                    "The current password is incorrect."
                )
                self.behavior.service_data.update({"success": False})
                return False

            # 3. Package payload
            sed = ServiceEntryData(
                service_data={
                    "method_name": "update_user_logins",
                    "pk": pk,
                    "password": new_password,
                    "service_args": {
                        "session_key": self.parent_service.session_key,
                        "load_record": False,
                    },
                }
            )

            # 4. Dispatch to Database
            success = self.parent_service.hook_pad("user_model_service", entry=sed)
            self.behavior.service_data.update({"success": success})
            return success
