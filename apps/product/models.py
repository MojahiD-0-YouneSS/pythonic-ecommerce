from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django_abstract.base.base_model import BaseModel, models, timezone
from django_abstract.registry import creator_selector
from apps.product.dependencies import ProductAppDependecy

@creator_selector(dependency=ProductAppDependecy)
class Product(BaseModel):
    """Represents a product with essential details and relationships."""
    reference_number = models.CharField(max_length=20, unique=True, null=True)
    name = models.CharField(max_length=255, unique=True, help_text="The product's name.")
    slug = models.SlugField(unique=True, max_length=255, help_text="SEO-friendly URL identifier.")
    description = models.TextField(blank=True, help_text="Full description of the product.")
    short_description = models.CharField(max_length=500, blank=True, help_text="Brief summary for listings.")
    sku = models.CharField(max_length=100, unique=True, help_text="Unique identifier for the product.")
    is_featured = models.BooleanField(default=False, help_text="Highlight as a featured product.")
    # brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True, help_text="Associated brand.")
    categories = models.ManyToManyField('Category', blank=True, related_name="products", help_text="Associated categories.")
    # collections = models.ManyToManyField('Collection', blank=True, related_name="products", help_text="Associated collections.")

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

@creator_selector(dependency=ProductAppDependecy)
class ProductVariant(BaseModel):
    """Represents a specific variant of a product."""
    reference_number = models.CharField(max_length=20, unique=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', help_text="Parent product.")
    slug = models.SlugField(unique=True, max_length=255, help_text="SEO-friendly URL identifier.")
    sku = models.CharField(max_length=100, unique=True,  null=True, blank=True, help_text="Unique SKU for the variant.")
    size = models.CharField(max_length=250,  null=True, blank=True, help_text="Size attribute.")
    color = models.CharField(max_length=250,  null=True, blank=True, help_text="Color attribute.")
    fabric = models.CharField(max_length=250,  null=True, blank=True, help_text="Fabric attribute.")
    weight = models.CharField(max_length=250,  null=True, blank=True, help_text="Weight attribute.")
    dimensions = models.CharField(max_length=250,  null=True, blank=True, help_text="Dimensions attribute.")
    stock = models.PositiveIntegerField(default=0, help_text="Quantity available in stock.")
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the variant.")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the variant.")
    is_active = models.BooleanField(default=True, help_text="Whether the variant is available for sale.")


    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(''.join([self.product.slug , self.color , self.size]))
        if not self.sku:
            self.sku = '-'.join([ self.product.sku, self.color , self.size])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

@creator_selector(dependency=ProductAppDependecy)
class Category(BaseModel):
    """Represents a hierarchical category structure."""
    name = models.CharField(max_length=255, unique=True, help_text="Category name.")
    slug = models.SlugField(unique=True, max_length=255, help_text="SEO-friendly URL identifier.")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories', help_text="Parent category for hierarchy.")
    description = models.TextField(blank=True, help_text="Description of the category.")
    image = models.ImageField(upload_to='categories/', blank=True, help_text="Category image.")

    def __str__(self):
        return self.name

@creator_selector(dependency=ProductAppDependecy)
class ProductImage(BaseModel):
    """Represents images for product variants."""
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images', help_text="Associated product variant.")
    image = models.ImageField(upload_to='product_images/', help_text="Image file.")
    alt_text = models.CharField(max_length=255, blank=True, help_text="Alternate text for the image.")
    is_primary = models.BooleanField(default=False, help_text="Whether the image is the primary image.")

    def __str__(self):
        return f"Image for {self.variant}"
 
@creator_selector(dependency=ProductAppDependecy)
class ReviewModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    replies_data = models.ManyToManyField('ReplyModel',  related_name='replies')
    def __str__(self):
        return f'Review by {self.user.username} - {self.rating} stars'

@creator_selector(dependency=ProductAppDependecy)
class ReplyModel(BaseModel):
    review = models.ForeignKey(ReviewModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    reply_data = models.TextField()
    is_active = models.BooleanField(default=True)

