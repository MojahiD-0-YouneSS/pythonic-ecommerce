from ..views.admin_views import custom_views
from ..views.admin_views import crud_views 
from django.urls import path

admin_urlpatterns = [
    path('admin/cart/client/', crud_views.AdminCartView.as_view(), name='admin_cart'),
    path('admin/discount', crud_views.AddDiscountCodeView.as_view(), name='admin_discount'),
]