from time import timezone
from django.views import View
from apps.cms.dependencies import get_cms_app_dependency
from apps.utility import CustomAdminRequiredMixin
from ui.pages.cms.admin.dashboard import DashboardPage
from ui.pages.cms.admin.site_content import SiteContentPage
from ui.pages.product.admin import product_dashboard_page
from ui.pages.client.admin.client_dashboard import ClientAdminDashboard
from ui.pages.order.admin.order_dashboard import OrderDashboardPage
from django.http import HttpResponse
from apps.product.dependencies import get_product_app_dependency
from apps.client.dependencies import get_client_dependency
from apps.order.models import Order
from django.utils import timezone
from datetime import timedelta
from django_abstract.utilities import HtmxLoginRequiredMixin, AdminOrStaffMixin
from probo.components import frag,Frag

class AdminDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        with request.ui_context:
            return HttpResponse(frag(DashboardPage()))

class AdminProductDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        with request.ui_context as ctx:
            products = get_product_app_dependency().select_product.access_db.filter(
                is_active=True,
            ).order_by('-id')
            
            from django.core.paginator import Paginator
            page_number = request.GET.get('page', 1)
            paginator = Paginator(products, 12)
            page_obj = paginator.get_page(page_number)
            
            ctx.put('all_products', products)
            ctx.put('products', page_obj.object_list)
            ctx.put('page_obj', page_obj)
            
            page = product_dashboard_page()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

class AdminClientDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        with request.ui_context as ctx:
            clients = get_client_dependency().select_client.access_db.all()
            ctx.put('clients', clients)

            now = timezone.now()
            start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
            one_week_ago = now - timedelta(days=7)

            stats = {
                "total": clients.count(),
                
                "active_today": clients.filter(user__last_login__lte=start_of_today).count(),
                
                "new_this_week": clients.filter(user__date_joined__gte=one_week_ago).count(),
            }

            # 3. Add to your context
            ctx.put("stats", stats)
            page = ClientAdminDashboard()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

class AdminOrderDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        with request.ui_context as ctx:
            orders = Order.objects.all()
            ctx.put('orders', orders)
            page = OrderDashboardPage()
            return HttpResponse(frag(Frag(page,data_pipeline=ctx)))

class AdminSiteDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        with request.ui_context as ctx:

            cmsd = get_cms_app_dependency()

            ctx.push(
                banners=cmsd.select_banner.access_db.all(),
                posters = cmsd.select_poster.access_db.all(),
                system_banners = cmsd.select_system_banner_rotation.access_db.all(),
                testimonies = cmsd.select_testimony.access_db.all(),
                about_us = cmsd.select_about_us.access_db.all(),
                quotes = cmsd.select_quote.access_db.all(),
                contacts = cmsd.select_contact.access_db.all(),
            )
            return HttpResponse(frag(Frag(SiteContentPage(),data_pipeline=ctx)))
