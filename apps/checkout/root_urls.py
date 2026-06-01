# checkout root_urls.py
from apps.checkout.urls.admin_urls import admin_urlpatterns
from apps.checkout.urls.client_urls import client_urlpatterns

app_name = "checkout"

urlpatterns = client_urlpatterns + admin_urlpatterns
