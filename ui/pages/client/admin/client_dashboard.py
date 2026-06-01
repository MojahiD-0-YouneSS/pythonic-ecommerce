from ui.pages.client.admin.client_listingns import AdminUserListingCard
from ui.pages.client.admin.client_report import AdminUserDetailCard
from ui.pages.client.admin.client_summary import UserManagementSummary
from ui.pages.base import get_management_base_template
from apps.global_context import get_global_context
from probo import DIV, H4, P, H5

def ClientAdminDashboard():
    """
    Orchestrator for the Client Admin Dashboard.
    Uses SSDOM finding logic to patch the management base template.
    """

    context = get_global_context()
    base = get_management_base_template()
    clients = context.get('clients', [])
    stats = context.get('stats', {}) # Assuming stats are in context
    
    # 1. Patch the Page Title
    base_title = base.html_doc.find(lambda n: n.tag == "TITLE")
    if base_title:
        base_title.inner_html('Users Dashboard!')

    # 2. Locate the main content area via SSDOM ID
    base_body = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )

    if base_body:
        # 3. Construct the layout using flat argument structure
        content = DIV(
            # Header
            DIV(
                H4("User Management Hub", Class="fw-bold mb-0"),
                P("Monitor and moderate your user ecosystem.", Class="text-muted small"),
                Class="mb-4"
            ),
            
            # Summary Metrics
            UserManagementSummary(stats),
            
            # Listing Grid
            DIV(
                H5("All Active Clients", Class="mb-3"),
                DIV(
                    *[AdminUserListingCard(client) for client in (clients if clients else [None])],
                    Class="d-flex flex-wrap gap-3"
                ),
                Class="p-4 bg-white border rounded shadow-sm"
            ),
            
            Class="p-5"
        )

        # 4. Add the composed content to the found body node
        base_body.add(content)

    return base
