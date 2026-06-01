from django.urls import path
from apps.order.views.admin_views import (
    crud_views,custom_views,partial_views
)
admin_url_patterns = [
    path(
        "manage/<uuid:order_id>/",
        crud_views.OrderManagementView.as_view(),
        name="admin_order_management",
    ),
    path(
        "process/<uuid:order_id>/",
        partial_views.OrderProssingView.as_view(),
        name="admin_order_processing",
    ),
    # Additional admin URLs can be added here
]
