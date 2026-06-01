import random
import uuid
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.apps import apps
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
from django.conf import settings

class Command(BaseCommand):
    help = (
        "Seeds all CMS models with realistic storefront data using exact schema fields."
    )

    def handle(self, *args, **kwargs):
        self.stdout.write("Wiping old CMS data...")

        Quote.objects.all().delete()
        SystemBannerRotation.objects.all().delete()
        HomepageEditor.objects.all().delete()
        Banner.objects.all().delete()
        Poster.objects.all().delete()
        Testimony.objects.all().delete()
        AboutUs.objects.all().delete()
        Contact.objects.all().delete()
        ContactUs.objects.all().delete()
        PageVisit.objects.all().delete()
        DashboardMetrics.objects.all().delete()

        now = timezone.now()

        # 1. BANNERS
        self.stdout.write("Creating Banners...")
        banners_data = [
            (
                "The Winter Collection",
                "Engineered for warmth, designed for style.",
                "http://localhost:8000/products/",
                "banner1.jpg",
            ),
            (
                "Tech Essentials",
                "Upgrade your daily workflow with our premium gear.",
                "http://localhost:8000/products/",
                "banner2.jpg",
            ),
            (
                "Spring Clearance",
                "Up to 40% off selected signature items.",
                "http://localhost:8000/sale/",
                "banner3.jpg",
            ),
        ]
        for idx, (title, subtitle, url, img) in enumerate(banners_data, 1):
            Banner.objects.create(
                title=title,
                subtitle=subtitle,
                url=url,
                image=f"media/banners/{img}",
                position=idx,
                alt_text=f"Promo for {title}",
                is_featured=True,
                is_active=True,
            )

        # 2. POSTERS
        self.stdout.write("Creating Posters...")
        posters_data = [
            (
                "Flash Sale Weekend",
                "Grab your favorites before they're gone.",
                "/sale/",
                "poster1.jpg",
            ),
            (
                "New Arrivals",
                "Check out what just landed in our catalog.",
                "/new/",
                "poster2.jpg",
            ),
        ]
        for idx, (title, desc, url, img) in enumerate(posters_data, 1):
            Poster.objects.create(
                title=title,
                description=desc,
                link_url=url,
                image=f"media/posters/{img}",
                priority=idx,
                is_featured=True,
                is_active=True,
            )

        # 3. ABOUT US
        self.stdout.write("Creating About Us...")
        AboutUs.objects.create(
            title="Crafting Elegance Through Python",
            content="We believe in building software and selling products that combine top-tier performance with beautiful aesthetics. Our platform is driven by a custom Domain-Driven Design engine.",
            image=f"media/about_us/about.jpg",
            call_to_action_text="Read Our Story",
            call_to_action_url="/about/",
            background_color="#ffffff",
            is_active=True,
        )

        # 4. SYSTEM BANNER ROTATION
        self.stdout.write("Creating System Banner Rotations...")
        SystemBannerRotation.objects.create(
            title="Holiday Season Promo",
            image=f"media/banners/holiday_sys.jpg",
            link="/holiday-sale/",
            display_from=now - timedelta(days=5),
            display_until=now + timedelta(days=30),
            is_active=True,
        )

        # 5. HOMEPAGE EDITOR
        self.stdout.write("Creating Homepage Editor configs...")
        HomepageEditor.objects.create(
            section_name="Hero Block",
            content_type="product_carousel",
            content_data={
                "config": {"autoplay": True, "speed": 500},
                "items": [1, 2, 3],
            },
            order=1,
            is_visible=True,
            is_active=True,
        )

        # 6. DASHBOARD METRICS
        self.stdout.write("Creating Dashboard Metrics...")
        metrics = [
            ("total_revenue", 45290.50, "Total Revenue generated this month"),
            ("active_users", 1250.0, "Current active users on platform"),
            ("bounce_rate", 34.5, "Percentage of users leaving after 1 page"),
        ]
        for key, val, desc in metrics:
            DashboardMetrics.objects.create(
                metric_key=key, metric_value=val, description=desc, is_active=True
            )

        # 7. PAGE VISITS
        self.stdout.write("Creating Page Visits...")
        for _ in range(20):
            PageVisit.objects.create(
                page_url=random.choice(
                    ["/home", "/products/", "/checkout/", "/about/"]
                ),
                session_id=uuid.uuid4().hex[:16],
                visit_duration=random.randint(10, 300),
                is_active=True,
            )

        # 8. CONTACT & CONTACT US
        self.stdout.write("Creating Contacts...")
        Contact.objects.create(
            full_name="John Doe",
            email="john@example.com",
            message="I am having trouble with my recent order tracking.",
            contact_reason="support",
            priority="high",
            is_active=True,
        )
        ContactUs.objects.create(
            full_name="Jane Smith",
            email="jane@example.com",
            subject="Bulk Pricing Inquiry",
            message="Do you offer discounts for bulk B2B purchases?",
            inquiry_type="sales",
            is_active=True,
        )

        # 9. FETCH FOREIGN KEYS FOR QUOTES AND TESTIMONIES
        # We need to grab a Client and a Product if they exist
        try:
            Client = apps.get_model("client", "Client")
            Product = apps.get_model("product", "Product")
            dummy_client = Client.objects.filter(is_active=True).first()
            dummy_product = Product.objects.filter(is_active=True).first()
        except LookupError:
            dummy_client = None
            dummy_product = None

        # 10. TESTIMONIES
        self.stdout.write("Creating Testimonies...")
        testimonies_data = [
            (
                "Sarah Jenkins",
                "Absolutely incredible quality. The checkout process was seamless!",
                5,
                "person1.png",
            ),
            (
                "Michael Chen",
                "I've never seen a storefront load this fast. Highly recommend.",
                4,
                "person2.png",
            ),
            (
                "Emma Watson",
                "Great customer service and fantastic product build quality.",
                5,
                "person3.png",
            ),
        ]
        for idx, (name, feedback, rating, img) in enumerate(testimonies_data, 1):
            Testimony.objects.create(
                customer_name=name,
                customer_image=f"media/testimonies/{img}",
                feedback=feedback,
                rating=rating,
                is_approved=True,
                highlighted=(idx == 1),  # Highlight the first one
                product=dummy_product,  # Attach product if we found one
                is_active=True,
            )

        # 11. QUOTES
        self.stdout.write("Creating Quotes...")
        if dummy_client and dummy_product:
            Quote.objects.create(
                customer=dummy_client,
                reference_code=f"QTE-{uuid.uuid4().hex[:6].upper()}",
                product=dummy_product,
                quantity=random.randint(5, 50),
                proposed_price=Decimal("1500.00"),
                status="pending",
                expires_at=now + timedelta(days=14),
                is_active=True,
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping Quotes: No active Client or Product found in DB. Run product/client seeders first!"
                )
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded all CMS Data!"))

        self.stdout.write(
            self.style.WARNING(
                "\n[ACTION REQUIRED]: For the images to render, place your image files in these exact paths:\n"
                "- media/banners/banner1.jpg\n"
                "- media/banners/banner2.jpg\n"
                "- media/banners/banner3.jpg\n"
                "- media/banners/holiday_sys.jpg\n"
                "- media/posters/poster1.jpg\n"
                "- media/posters/poster2.jpg\n"
                "- media/about_us/about.jpg\n"
                "- media/testimonies/person1.png\n"
                "- media/testimonies/person2.png\n"
                "- media/testimonies/person3.png\n"
            )
        )
