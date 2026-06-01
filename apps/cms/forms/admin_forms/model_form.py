from django_abstract.base.base_form import BaseForm 
from apps.cms.models import (
    Quote,
    SystemBannerRotation,
    HomepageEditor,
    Banner,
    Poster,
    Testimony,
    AboutUs,
    Contact,
    ContactUs,
    PageVisit,
    DashboardMetrics,
)


class QuoteForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Quote

class SystemBannerRotationForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = SystemBannerRotation

class HomepageEditorForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = HomepageEditor

class BannerForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Banner

class PosterForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Poster

class TestimonyForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Testimony

class AboutUsForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = AboutUs

class ContactForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Contact

class ContactUsForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = ContactUs

class PageVisitForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = PageVisit

class DashboardMetricsForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = DashboardMetrics