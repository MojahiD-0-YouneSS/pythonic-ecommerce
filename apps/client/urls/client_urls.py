from apps.client.views.client_views import (
    custom_views , crud_views , partial_views
)
from django.urls import path

client_urlpatterns = [
    path("auth/login/", crud_views.ClientLoginView.as_view(), name="login"),
    path("auth/signup/", crud_views.ClientSignupView.as_view(), name="signup"),
    path("auth/logout/", crud_views.ClientLogoutView.as_view(), name="logout"),
    # --- Profile Endpoints ---
    # GET (read), POST (create), PUT (update)
    path("profile/", crud_views.ClientProfileView.as_view(), name="profile_base"),
    path(
        "profile/info/",
        partial_views.ClientProfileInfoView.as_view(),
        {"is_disabled": 1},
        name="profile-info-default",
    ),
    path(
        "profile/info/<int:is_disabled>/",
        partial_views.ClientProfileInfoView.as_view(),
        name="profile-info",
    ),
    path(
        "profile/info/logins/",
        partial_views.ClientLoginInfoView.as_view(),
        {"is_disabled": 1},
        name="profile-login-default",
    ),
    path(
        "profile/info/logins/<int:is_disabled>/",
        partial_views.ClientLoginInfoView.as_view(),
        name="profile-login",
    ),
    # path("profile/<int:id>/", crud_views.ClientProfileView.as_view(), name="profile_detail"),
    # --- Shopping History Endpoints ---
    # GET (read)
    path("history/", crud_views.ShoppingHistoryView.as_view(), name="history_list"),
    path(
        "history/<int:id>/",
        crud_views.ShoppingHistoryView.as_view(),
        name="history_detail",
    ),
]
