from django.urls import path 
from apps.order.views.client_views import (
    crud_views, custom_views, partial_views
)

client_url_patterns = [
    path("history/", partial_views.OrderHistoryView.as_view(), name="order-history"),
    path(
        "billing/address/",
        partial_views.AddressBookView.as_view(),
        name="billing-address",
    ),
    path(
        "add/address/",
        partial_views.AddAddressView.as_view(),
        name="add-billing-address",
    ),path(
        "order/detail/<uuid:order_id>",
        partial_views.OrderDetailView.as_view(),
        name="order_detail",
    ),
]
