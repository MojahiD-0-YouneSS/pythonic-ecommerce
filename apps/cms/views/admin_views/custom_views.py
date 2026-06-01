from time import timezone
from django.views import View
from apps.cms.dependencies import get_cms_app_dependency
from apps.utility import CustomAdminRequiredMixin
from ui.pages.cms.admin.dashboard import DashboardPage
from ui.pages.cms.admin.site_content import SiteContentPage
from ui.pages.product.admin import product_dashboard_page
from ui.pages.client.admin.client_dashboard import ClientAdminDashboard
from ui.pages.order.admin.order_dashboard import OrderDashboardPage
from apps.global_context import get_global_context
from django.http import HttpResponse
from apps.product.dependencies import get_product_app_dependency
from apps.client.dependencies import get_client_dependency
from apps.order.models import Order
from django.utils import timezone
from datetime import timedelta
from django_abstract.utilities import HtmxLoginRequiredMixin, AdminOrStaffMixin

class AdminDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()

    def get(self, request, *args, **kwargs):
        
        return HttpResponse(DashboardPage().render())

class AdminProductDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()

    def get(self, request, *args, **kwargs):
        with self.__ctx as ctx:
            products = get_product_app_dependency().select_product.access_db.filter(
                is_active=True,
            )
            ctx.put('products', products)
            page = product_dashboard_page()
        return HttpResponse(page.render())

class AdminClientDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()

    def get(self, request, *args, **kwargs):
        with self.__ctx as ctx:
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
            return HttpResponse(page.render())

class AdminOrderDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()

    def get(self, request, *args, **kwargs):
        with self.__ctx as ctx:
            orders = Order.objects.all()
            ctx.put('orders', orders)
            page = OrderDashboardPage()
        return HttpResponse(page.render())

class AdminSiteDashboardView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()

    def get(self, request, *args, **kwargs):
        with self.__ctx as ctx:

            cmsd = get_cms_app_dependency()
            banners = cmsd.select_banner.access_db.all()
            posters = cmsd.select_poster.access_db.all()
            system_banners = cmsd.select_system_banner_rotation.access_db.all()
            testimonies = cmsd.select_testimony.access_db.all()
            about_us = cmsd.select_about_us.access_db.all()
            quotes = cmsd.select_quote.access_db.all()
            contacts = cmsd.select_contact.access_db.all()
            ctx.push(
                **{
                    'banners': banners,
                    'posters': posters,
                    'system_banners': system_banners,
                    'testimonies': testimonies,
                    'about_us': about_us,
                    'quotes': quotes,
                    'contacts': contacts,
                }
            )
            page = SiteContentPage()
        return HttpResponse(page.render())
