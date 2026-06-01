from django.urls import path
from apps.checkout.views.client_views import (
    crud_views,custom_views
)
client_urlpatterns = [
    path("client/process/", crud_views.ProcessCheckoutView.as_view(), name="process_checkout"),
]
