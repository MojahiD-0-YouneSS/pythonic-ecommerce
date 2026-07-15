from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, IMG, H4
from probo.components import Frag
from django.urls import reverse

def UserManagementSummary():
    """
    A high-level summary dashboard for User Management.
    stats = {'total': int, 'active_today': int, 'new_this_week': int}
    """

    return Frag(
        # Block 1: Total Registered
        DIV(
            DIV(
                I(Class="bi bi-people fs-1 text-primary"),
                DIV(
                    H4({'stats.total'}, Class="mb-0 fw-bold"),
                    P("Total Registered", Class="text-muted mb-0 small"),
                    Class="ms-3"
                ),
                Class="d-flex align-items-center"
            ),
            Class="col-md-4 p-4 border-end"
        ),
        # Block 2: Active Today
        DIV(
            DIV(
                I(Class="bi bi-person-check fs-1 text-success"),
                DIV(
                    H4({'stats.active_today'}, Class="mb-0 fw-bold"),
                    P("Active Today", Class="text-muted mb-0 small"),
                    Class="ms-3"
                ),
                Class="d-flex align-items-center"
            ),
            Class="col-md-4 p-4 border-end"
        ),
        # Block 3: New Customers
        DIV(
            DIV(
                I(Class="bi bi-person-plus fs-1 text-info"),
                DIV(
                    H4({'stats.new_this_week'}, Class="mb-0 fw-bold"),
                    P("New Customers", Class="text-muted mb-0 small"),
                    Class="ms-3"
                ),
                Class="d-flex align-items-center"
            ),
            Class="col-md-4 p-4"
        )
    )
