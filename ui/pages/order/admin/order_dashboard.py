from probo import DIV, H5, H6, P, SPAN, BUTTON, I, SMALL, A, SECTION, HR,H4
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from ui.components.order.admin.active_orders import ActiveOrderCard
from ui.components.order.admin.ready_to_diliver import ReadyToDeliverCard
from ui.components.order.admin.listing_all import OrderListRow
from ui.pages.base import get_management_base_template
from probo.components import Frag

def OrderDashboard():
    """
    Full Order Operations Dashboard.
    orders: QuerySet of all orders.
    """
    # System logic within component
    def active_orders(**dvars)->DIV:
        orders = dvars.get('orders',[]) or []
        active = [Frag(ActiveOrderCard(),data_pipeline={'order':o}) for o in orders if o.status in ['Pending', 'Processing']]
        return DIV(*active, Class="d-flex flex-wrap gap-3") if active else P("No active orders.", Class="text-muted small")
    def ready_orders(**dvars)->DIV:
        orders = dvars.get('orders', []) or []
        ready = [Frag(ReadyToDeliverCard(),data_pipeline={'order':o}) for o in orders if o.status == 'Processing' and o.payment_status == 'Paid']
        return DIV(*ready, Class="d-flex flex-column gap-2") if ready else P("Nothing to ship yet.", Class="text-muted small")
    def order_list(**dvars)->DIV:
        orders = dvars.get('orders',[]) or []
        return DIV(*[Frag(OrderListRow(),data_pipeline={'order':o}) for o in (orders[:20] if orders else [])])
    return DIV(
        # Page Header
        DIV(
            H4("Order Fulfillment Hub", Class="fw-bold"),
            P("Manage active shipments, pending payments, and order verification.", Class="text-muted small"),
            Class="mb-5"
        ),

        # Top Row: Kanban-style buckets
        DIV(
            # Column 1: Active Handlers
            SECTION(
                H5("Incoming & Processing", Class="mb-4 text-primary fs-6 fw-bold"),
                {'orders',active_orders},
                Class="col-lg-8"
            ),
            # Column 2: Fulfillment Queue
            SECTION(
                H5("Ready to Ship", Class="mb-4 text-success fs-6 fw-bold"),
                {'orders',ready_orders},
                Class="col-lg-4 ps-lg-4 border-start"
            ),
            Class="row mb-5"
        ),

        HR(Class="my-5"),

        # Bottom Section: Master List
        SECTION(
            H5("Master Order Registry", Class="mb-4"),
            DIV(
                # Table Header
                DIV(
                    DIV("ID", Class="col-1 fw-bold small text-muted"),
                    DIV("Customer", Class="col-2 fw-bold small text-muted"),
                    DIV("Date Placed", Class="col-2 fw-bold small text-muted"),
                    DIV("Status", Class="col-2 fw-bold small text-muted"),
                    DIV("Total", Class="col-1 fw-bold small text-muted"),
                    DIV("Payment", Class="col-2 fw-bold small text-muted text-center"),
                    DIV("Actions", Class="col-2 fw-bold small text-muted text-end"),
                    Class="row py-2 px-3 bg-light border rounded-top g-0"
                ),
                # Rows
                {'orders',order_list},
                Class="bg-white border rounded-bottom"
            )
        ),
        
        Class="container-fluid py-4",
        id="order-admin-dashboard"
    )

def OrderDashboardPage():

    base =  get_management_base_template()
    base_title = base.html_doc.find(lambda n:n.tag == "TITLE")
    if base_title:
        base_title.inner_html("Order Dashboard")
    base_body = base.html_doc.find(
        lambda n: n.attr_manager.get_attr("data_ssdom_id") == "root-container"
    )
    if base_body:
        base_body.add(OrderDashboard())
    return base    
