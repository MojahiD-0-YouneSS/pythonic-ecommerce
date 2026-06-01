# product root_urls.py
from apps.product.urls.admin_urls import admin_urlpatterns
from apps.product.urls.client_urls import client_urlpatterns

app_name="product"
urlpatterns = admin_urlpatterns + client_urlpatterns
