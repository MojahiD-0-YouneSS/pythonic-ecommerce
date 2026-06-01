from django.urls import path
from apps.product.views.admin_views import (
    crud_views,
    custom_views,
)


admin_urlpatterns = [
    path("add/product/", crud_views.AddProductView.as_view(), name="product"),
    path("add/variant/", crud_views.AddProductVariantView.as_view(), name="variant"),
    path("add/image/", crud_views.AddProductImageView.as_view(), name="image"),
    path("add/category/", crud_views.AddProductCategoryView.as_view(), name="category"),
    path("add/review/", crud_views.AddProductReviewView.as_view(), name="review"),
    path("add/reply/", crud_views.AddProductReplyView.as_view(), name="reply"),
    path("list/products/", crud_views.ProductListView.as_view(), name="products"),
    path(
        "detail/product/<uuid:product_id>/",
        crud_views.ProductDetailView.as_view(),
        name="admin-product-detail",
    ),
    path(
        "edit/product/<uuid:product_id>/",
        crud_views.ProductEditView.as_view(),
        name="admin-product-edit",
    ),
    path(
        "delete/product/<uuid:product_id>/",
        crud_views.ProductDeleteView.as_view(),
        name="admin-product-delete",
    ),
    path(
        "edit/product/variant/<uuid:product_id>/",
        crud_views.ProductVariantEditView.as_view(),
        name="admin-productvariant-edit",
    ),
    path(
        "delete/product/variant/<uuid:product_id>/",
        crud_views.ProductVariantDeleteView.as_view(),
        name="admin-productvariant-delete",
    ),
]
