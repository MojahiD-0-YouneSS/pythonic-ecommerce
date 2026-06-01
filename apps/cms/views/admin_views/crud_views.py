from apps.utility import CustomAdminRequiredMixin
from ui.pages.cms.admin.banner_form import AdminBannerFormPage
from django.views import View
from apps.global_context import get_global_context
from django.http import HttpResponse
from apps.cms.forms.admin_forms.model_form import BannerForm
from django_abstract.utilities import AdminOrStaffMixin, HtmxLoginRequiredMixin


class AdminBannerCreateView(HtmxLoginRequiredMixin, CustomAdminRequiredMixin, View):
    __ctx = get_global_context()
    def get(self,request):

        form = BannerForm()
        with self.__ctx as ctx:
            ctx.put("url","/cms/admin/add/form/")
            page = AdminBannerFormPage(form)
        return HttpResponse(page.render())    
