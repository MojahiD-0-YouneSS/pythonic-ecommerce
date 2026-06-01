from ..views.admin_views import custom_views
from ..views.admin_views import crud_views 
from django.urls import path

admin_urlpatterns = [
    path('admin/client/', crud_views.AdminClientView.as_view(), name='admin_client'),
    path('admin/guest_identity/', crud_views.GuestIdentityView.as_view(), name='guest_identity'),
    path('admin/client_detail/<uuid:user_id>/', crud_views.ClientDetailView.as_view(), name='client_detail'),
]