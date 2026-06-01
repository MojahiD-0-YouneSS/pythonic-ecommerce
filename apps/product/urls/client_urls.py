from django.urls import path
from apps.product.views.client_views import (
    crud_views,
    custom_views,
    partial_views,
)

client_urlpatterns = [
    path('products/', crud_views.ProductCatalogView.as_view(), name='product-catalog'),
    path('products/filter/', partial_views.ProductFilterView.as_view(), name='product-filter'),
    path('detail/<uuid:product_id>/', crud_views.ProductDetailView.as_view(), name='product-detail'),
]