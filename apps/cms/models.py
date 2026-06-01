from django.db import models
from django_abstract.base.base_model import BaseModel, timezone
from django_abstract.registry import creator_selector
from apps.cms.dependencies import CmsAppDependency

# Create your models here.


@creator_selector(dependency=CmsAppDependency)
class Quote(BaseModel):
    customer = models.ForeignKey("client.Client", on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=20, unique=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ], default='pending')
    expires_at = models.DateTimeField(null=True, blank=True)

@creator_selector(dependency=CmsAppDependency)
class SystemBannerRotation(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    display_from = models.DateTimeField()
    display_until = models.DateTimeField()

    class Meta:
        ordering = ['-display_from']

@creator_selector(dependency=CmsAppDependency)
class HomepageEditor(BaseModel):
    section_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('product_carousel', 'Product Carousel'),
    ])
    content_data = models.JSONField()
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

@creator_selector(dependency=CmsAppDependency)
class Banner(BaseModel):
    """
    Model to represent promotional or informational banners on the platform.
    """
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='banners/')
    url = models.URLField(blank=True)
    position = models.IntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True)


    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)


    def is_visible(self):
        """
        Determines whether the banner is currently visible based on dates and active status.
        """
        now = timezone.now()
        return (
            self.is_active and
            (self.start_date is None or self.start_date <= now) and
            (self.end_date is None or self.end_date >= now)
        )

    class Meta:
        ordering = ['position', '-created_at']
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'

    def __str__(self):
        return f"{self.title}"

@creator_selector(dependency=CmsAppDependency)
class Poster(BaseModel):
    """
    Model to manage posters for events, promotions, or announcements.
    """
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='posters/')
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    link_url = models.URLField(blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True)


    def is_visible(self):
        """
        Checks if the poster is currently visible based on its active status and date range.
        """
        now = timezone.now()
        return (
            self.is_active and
            (self.start_date is None or self.start_date <= now) and
            (self.end_date is None or self.end_date >= now)
        )

    class Meta:
        ordering = ['priority', '-created_at']
        verbose_name = 'Poster'
        verbose_name_plural = 'Posters'

    def __str__(self):
        return f"{self.title} - {'Visible' if self.is_visible() else 'Hidden'}"

@creator_selector(dependency=CmsAppDependency)
class Testimony(BaseModel):
    """
    Model to manage customer testimonials or feedback.
    """
    customer_name = models.CharField(max_length=255)
    customer_image = models.ImageField(
        upload_to='testimonies/', blank=True, null=True
    )
    feedback = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5, choices=[(i, i) for i in range(1, 6)]
    )
    product = models.ForeignKey(
        'product.Product', on_delete=models.SET_NULL, null=True, blank=True
    )
    is_approved = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    highlighted = models.BooleanField(default=False)


    def __str__(self):
        return f"Testimony by {self.customer_name} ({'Approved' if self.is_approved else 'Pending Approval'})"


    class Meta:
        ordering = ['-highlighted', 'display_order', '-created_at']
        verbose_name = 'Testimony'
        verbose_name_plural = 'Testimonies'


    def rating_stars(self):
        """
        Returns a visual representation of the rating as stars.
        """
        return '⭐' * self.rating + '☆' * (5 - self.rating)

    def is_visible(self):
        """
        Checks if the testimony is approved and active.
        """
        return self.is_active and self.is_approved
    def is_highlighted(self):
        """
        Checks if the testimony is highlighted.
        """
        return self.highlighted
    def is_product_related(self):
        """
        Checks if the testimony is related to a specific product.
        """
        return self.product is not None

@creator_selector(dependency=CmsAppDependency)
class AboutUs(BaseModel):
    """
    Model to manage the About Us page content.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='about_us/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)
    background_color = models.CharField(max_length=7, blank=True, null=True)
    call_to_action_text = models.CharField(max_length=255, blank=True, null=True)
    call_to_action_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'About Us Section'
        verbose_name_plural = 'About Us Sections'

    def __str__(self):
        return self.title

    def is_video_embeddable(self):
        """
        Checks if the video URL is from a known embeddable source (e.g., YouTube, Vimeo).
        """
        if self.video_url:
            return "youtube.com" in self.video_url or "vimeo.com" in self.video_url
        return False

@creator_selector(dependency=CmsAppDependency)
class Contact(BaseModel):
    """
    Model to handle contact inquiries from users or customers.
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    responded = models.BooleanField(default=False)
    response_message = models.TextField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)
    contact_reason = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Inquiry'),
            ('support', 'Support Request'),
            ('feedback', 'Feedback'),
            ('other', 'Other'),
        ],
        default='general'
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        default='medium'
    )
    attachment = models.FileField(upload_to='contact_attachments/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'

    def __str__(self):
        return f"{self.full_name} - {'Responded' if self.responded else 'Pending'}"

    def mark_as_responded(self, response_message=None):
        """
        Marks the contact inquiry as responded, with an optional response message.
        """
        self.responded = True
        self.response_date = timezone.now()
        if response_message:
            self.response_message = response_message
        self.save()

    def is_urgent(self):
        """
        Checks if the contact inquiry is marked as urgent.
        """
        return self.priority == 'urgent'

@creator_selector(dependency=CmsAppDependency)
class ContactUs(BaseModel):
    """
    Model to manage inquiries from the 'Contact Us' form.
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    inquiry_type = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Inquiry'),
            ('support', 'Support Request'),
            ('sales', 'Sales Inquiry'),
            ('feedback', 'Feedback'),
            ('other', 'Other'),
        ],
        default='general'
    )
    attachment = models.FileField(upload_to='contact_us_attachments/', blank=True, null=True)
    responded = models.BooleanField(default=False)
    response_message = models.TextField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Us Inquiry'
        verbose_name_plural = 'Contact Us Inquiries'

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

    def mark_as_responded(self, response_message=None):
        """
        Marks the inquiry as responded, optionally adding a response message.
        """
        self.responded = True
        self.response_date = timezone.now()
        if response_message:
            self.response_message = response_message
        self.save()

@creator_selector(dependency=CmsAppDependency)
class PageVisit(BaseModel):
    page_url = models.URLField(max_length=2000)
    session_id = models.CharField(max_length=255)
    visit_duration = models.PositiveIntegerField(null=True, blank=True)  # in seconds
    timestamp = models.DateTimeField(auto_now_add=True)

@creator_selector(dependency=CmsAppDependency)
class DashboardMetrics(BaseModel):
    metric_key = models.CharField(max_length=100, unique=True)
    metric_value = models.FloatField()
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
