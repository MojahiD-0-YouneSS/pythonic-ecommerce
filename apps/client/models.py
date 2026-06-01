from django_abstract.base.base_model import BaseModel, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_abstract.registry import creator_selector
from apps.client.dependencies import ClientAppDependency
from django.contrib.auth import get_user_model
from apps.client.dependencies import ClientAppDependency

# Instantiating ClientAppDependency inside the decorator parameters

User = get_user_model()

# Manual decorator invocation!
# This runs the registry wrapper over Django's default User model dynamically.
creator_selector(dependency=ClientAppDependency)(User)

@creator_selector(dependency=ClientAppDependency)
class Client(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    
    session_key = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique identifier for the guest's session."
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Client's phone number, including country code."
    )
    nickname = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique identifier for the guest's name."
    )
    preferred_language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('fr', 'French'),
            ('es', 'Spanish'),
            ('ar', 'Arabic'),
            ('zh', 'Chinese'),
            ('tm', 'Tamazight'),
        ],
        default='en',
        help_text="Preferred language for communication."
    )
    profile_picture = models.ImageField(
        upload_to='clients/profile_pictures/',
        blank=True,
        null=True,
        help_text="Profile picture of the client."
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Client's primary address."
    )
    profile_completion = models.PositiveIntegerField(
        default=0,
        help_text="Tracks percentage of profile completeness (0-100)."
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Indicates if the client's account is verified."
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        indexes = [
            models.Index(fields=['user', 'preferred_language']),
            models.Index(fields=['is_verified']),
        ]

    def __str__(self):
        return f"Client: {self.user.username}"

    def calculate_profile_completion(self):
        """Calculate the percentage of profile completion."""
        fields = [self.phone_number, self.preferred_language, self.profile_picture, self.address]
        completed_fields = sum(1 for field in fields if field)
        total_fields = len(fields)
        self.profile_completion = int((completed_fields / total_fields) * 100)

    def save(self, *args, **kwargs):
        """Override save method to ensure profile completion is calculated."""
        self.calculate_profile_completion()
        super().save(*args, **kwargs)

@creator_selector(dependency=ClientAppDependency)
class ClientProfile(BaseModel):
    """Core model for authenticated client profiles"""
    class ClientStatus(models.TextChoices):
        ACTIVE = 'ACT', 'Active'
        INACTIVE = 'INA', 'Inactive'
        SUSPENDED = 'SUS', 'Suspended'
        PENDING = 'PEN', 'Pending Verification'
        BLACKLISTED = 'BLK', 'Blacklisted'

    session_key = models.CharField(
        max_length=100,
        db_index=True,
        help_text="The user's session key whose preferences are being tracked."
    )
    status = models.CharField(
        max_length=3,
        choices=ClientStatus.choices,
        default=ClientStatus.PENDING
    )
    profile_picture = models.URLField(blank=True)
    last_active = models.DateTimeField(null=True, blank=True)
    acquisition_channel = models.CharField(max_length=50, blank=True)  # e.g., 'organic', 'paid', 'referral'
    acquisition_source = models.CharField(max_length=100, blank=True)  # e.g., 'google-ads', 'linkedin'
    internal_notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"
        indexes = [
            models.Index(fields=['status']),
            # models.Index(fields=['tier']),
            models.Index(fields=['last_active']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_status_display()})"

@creator_selector(dependency=ClientAppDependency)
class ShoppingHistory(BaseModel):
    session_key = models.CharField(
        max_length=100,
        db_index=True,
        help_text="The user's session key whose preferences are being tracked."
    )
    order =models.ForeignKey("order.Order", verbose_name=_("orders"),
        on_delete=models.SET_NULL,
        null=True,
        related_name='purchased_by',
        help_text="The product that was purchased."
    )
    ordered_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp when the purchase was made."
    )
    total_spent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        help_text="The total cost of the purchase (price * quantity)."
    )

    def __str__(self):
        return f"{self.order} placed by {self.user.user.username} on {self.created_at}"

@creator_selector(dependency=ClientAppDependency)
class GuestIdentity(BaseModel):
    session_key = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique identifier for the guest's session."
    )
    nickname = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique identifier for the guest's name."
    )
    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
        help_text="Optional email address provided by the guest."
    )
    last_active_at = models.DateTimeField(
        auto_now=True,
        help_text="Tracks the last time the guest was active."
    )
    is_converted = models.BooleanField(
        default=False,
        help_text="Indicates whether the guest has converted into a registered user."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or metadata about the guest."
    )

    class Meta:
        verbose_name = "Guest Client"
        verbose_name_plural = "Guest Clients"
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['email']),
            models.Index(fields=['is_converted']),
        ]

    def __str__(self):
        return f"Guest Client: {self.session_key}"
