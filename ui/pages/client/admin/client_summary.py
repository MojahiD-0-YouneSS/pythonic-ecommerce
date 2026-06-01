from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, IMG, H4
from django.urls import reverse

def UserManagementSummary(stats):
    """
    A high-level summary dashboard for User Management.
    stats = {'total': int, 'active_today': int, 'new_this_week': int}
    """
    
    print("Rendering UserManagementSummary with stats:", stats)
    
    return DIV(
        DIV(
            DIV(
                I(Class="bi bi-people fs-1 text-primary"),
                DIV(
                    H4(str(stats.get('total', 0)), Class="mb-0 fw-bold"),
                    P("Total Registered", Class="text-muted mb-0 small"),
                    Class="ms-3"
                ),
                Class="d-flex align-items-center"
            ),
            Class="col-md-4 p-4 border-end"
        ),
        DIV(
            DIV(
                I(Class="bi bi-person-check fs-1 text-success"),
                DIV(
                    H4(str(stats.get('active_today', 0)), Class="mb-0 fw-bold"),
                    P("Active Today", Class="text-muted mb-0 small"),
                    Class="ms-3"
                ),
                Class="d-flex align-items-center"
            ),
            Class="col-md-4 p-4 border-end"
        ),
        DIV(
            DIV(
                I(Class="bi bi-person-plus fs-1 text-info"),
                DIV(
                    H4(str(stats.get('new_this_week', 0)), Class="mb-0 fw-bold"),
                    P("New Customers", Class="text-muted mb-0 small"),
                    Class="ms-3"
                ),
                Class="d-flex align-items-center"
            ),
            Class="col-md-4 p-4"
        ),
        Class="row g-0 bg-white rounded shadow-sm border mb-5 overflow-hidden"
    )