# order root_urls.py
from apps.order.urls.client_urls import client_url_patterns
from apps.order.urls.admin_urls import admin_url_patterns
app_name = 'order'
urlpatterns = client_url_patterns+admin_url_patterns
