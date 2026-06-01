# cart root_urls.py
from .urls import(
    admin_urls,
    client_urls
)
app_name = 'cms'
urlpatterns = admin_urls.admin_urlpatterns+client_urls.client_urlpatterns