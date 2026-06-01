from apps.cms.views.client_views import (
    custom_views,
    crud_views,
) 
from django.urls import path

client_urlpatterns = [
    path("", crud_views.HomePageView.as_view(), name="home"),
    # --- Quote ---
    path("cms/quote/", custom_views.QuoteView.as_view(), name="quote_list"),
    path("cms/quote/<int:id>/", custom_views.QuoteView.as_view(), name="quote_detail"),
    # --- System Banner Rotation ---
    path("cms/system-banner-rotation/",
        custom_views.SystemBannerRotationView.as_view(),
        name="system_banner_rotation_list",
    ),
    path("cms/system-banner-rotation/<int:id>/",
        custom_views.SystemBannerRotationView.as_view(),
        name="system_banner_rotation_detail",
    ),
    # --- Homepage Editor ---
    path("cms/homepage-editor/",
        custom_views.HomepageEditorView.as_view(),
        name="homepage_editor_list",
    ),
    path("cms/homepage-editor/<int:id>/",
        custom_views.HomepageEditorView.as_view(),
        name="homepage_editor_detail",
    ),
    # --- Banner ---
    path("cms/banner/", custom_views.BannerView.as_view(), name="banner_list"),
    path("cms/banner/<int:id>/", custom_views.BannerView.as_view(), name="banner_detail"),
    # --- Poster ---
    path("cms/poster/", custom_views.PosterView.as_view(), name="poster_list"),
    path("cms/poster/<int:id>/", custom_views.PosterView.as_view(), name="poster_detail"),
    # --- Testimony ---
    path("cms/testimony/", custom_views.TestimonyView.as_view(), name="testimony_list"),
    path("cms/testimony/<int:id>/",
        custom_views.TestimonyView.as_view(),
        name="testimony_detail",
    ),
    # --- About Us ---
    path("cms/about-us/", custom_views.AboutUsView.as_view(), name="about_us_list"),
    path("cms/about-us/<int:id>/", custom_views.AboutUsView.as_view(), name="about_us_detail"
    ),
    # --- Contact ---
    path("cms/contact/", custom_views.ContactView.as_view(), name="contact_list"),
    path("cms/contact/<int:id>/", custom_views.ContactView.as_view(), name="contact_detail"
    ),
    # --- Contact Us ---
    path("cms/contact-us/", custom_views.ContactUsView.as_view(), name="contact_us_list"),
    path("cms/contact-us/<int:id>/",
        custom_views.ContactUsView.as_view(),
        name="contact_us_detail",
    ),
    # --- Page Visit ---
    path("cms/page-visit/", custom_views.PageVisitView.as_view(), name="page_visit_list"),
    path("cms/page-visit/<int:id>/",
        custom_views.PageVisitView.as_view(),
        name="page_visit_detail",
    ),
    # --- Dashboard Metrics ---
    path("cms/dashboard-metrics/",
        custom_views.DashboardMetricsView.as_view(),
        name="dashboard_metrics_list",
    ),
    path("cms/dashboard-metrics/<int:id>/",
        custom_views.DashboardMetricsView.as_view(),
        name="dashboard_metrics_detail",
    ),
]
