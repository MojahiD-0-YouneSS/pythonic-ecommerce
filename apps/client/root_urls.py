# client root_urls.py
# cart root_urls.py
from .urls import(
    admin_urls,
    client_urls,
    staff_urls
)
app_name = 'client'
urlpatterns = (
    admin_urls.admin_urlpatterns
    + client_urls.client_urlpatterns
    + staff_urls.staff_urlpatterns
)
