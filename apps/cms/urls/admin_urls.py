from django.urls import path
from apps.cms.views.admin_views import (
    crud_views,
    custom_views,
    partial_views,
)

app_name = 'cms'
admin_urlpatterns = [
    path('cms/admin/dashboard/', custom_views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('cms/admin/products/dashboard/', custom_views.AdminProductDashboardView.as_view(), name='admin-products-dashboard'),
    path('cms/admin/clients/dashboard/', custom_views.AdminClientDashboardView.as_view(), name='admin-clients-dashboard'),
    path('cms/admin/orders/dashboard/', custom_views.AdminOrderDashboardView.as_view(), name='admin-orders-dashboard'),
    path('cms/admin/content/dashboard/', custom_views.AdminSiteDashboardView.as_view(), name='admin-site-content'),
    path('cms/admin/add/banner/', crud_views.AdminBannerCreateView.as_view(), name='admin-banner-create'),
    path('cms/admin/add/poster/', crud_views.AdminPosterCreateView.as_view(), name='admin-poster-create'),
    path('cms/admin/add/system-banner/', crud_views.AdminSystemBannerCreateView.as_view(), name='admin-systembanner-create'),
    path('cms/admin/add/testimony/', crud_views.AdminTestimonyCreateView.as_view(), name='admin-testimony-create'),
    path('cms/admin/add/about-us/', crud_views.AdminAboutUsCreateView.as_view(), name='admin-aboutus-create'),
    path('cms/admin/hide/media/<str:slug>/<uuid:id>/', partial_views.HideMediaAdminCardView.as_view(), name='admin-hide-media'),
    path('cms/admin/edit/media/<str:slug>/<uuid:id>/', partial_views.EditMediaAdminCardView.as_view(), name='admin-edit-media'),
    path('cms/admin/delete/media/<str:slug>/<uuid:id>/', partial_views.DeleteMediaAdminCardView.as_view(), name='admin-delete-media'),
]