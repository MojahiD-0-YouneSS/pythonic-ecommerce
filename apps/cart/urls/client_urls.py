from ..views.client_views import custom_views
from ..views.client_views import crud_views 
from ..views.client_views import partial_views 
from django.urls import path

client_urlpatterns = [
    path("", crud_views.CartView.as_view(), name="cart"),
    path(
        "add/<uuid:product_id>",
        partial_views.AddToCartView.as_view(),
        name="add_to_cart",
    ),
    path(
        "remove/<uuid:item_id>",
        partial_views.RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path(
        "edit/<uuid:item_id>",
        partial_views.UpdateItemQuantityView.as_view(),
        name="edit-cart-item",
    ),
    path("discount/code/", crud_views.DiscountCodeView.as_view(), name="discount"),
]
