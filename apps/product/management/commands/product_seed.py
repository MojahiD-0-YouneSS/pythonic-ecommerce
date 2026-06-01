import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.product.models import Category, Product, ProductVariant, ProductImage


class Command(BaseCommand):
    help = (
        "Seeds 20 Categories, 20 Products, and 200 Variants with dynamic remote images."
    )

    def handle(self, *args, **kwargs):
        self.stdout.write("Wiping old product catalog data...")
        ProductImage.objects.all().delete()
        ProductVariant.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        # We will use an external URL for placeholders to save you from downloading 200 images.
        # Picsum provides beautiful, random, high-quality photos.
        def get_random_image_url(width=600, height=800, seed=None):
            # Using a seed ensures the same image stays assigned to the same product on refresh
            if not seed:
                seed = random.randint(1, 1000)
            return f"https://picsum.photos/seed/{seed}/{width}/{height}"

        # 1. Create 20 Categories
        self.stdout.write("Creating 20 Categories...")
        categories = []
        for i in range(1, 21):
            cat = Category.objects.create(
                name=f"Premium Category {i}",
                slug=f"premium-category-{i}",
                description="A fantastic collection of premium items.",
                is_active=True,
            )
            categories.append(cat)

        # 2. Create 20 Products (1 per Category)
        self.stdout.write("Creating 20 Products...")
        products = []
        for i, cat in enumerate(categories, 1):
            prod = Product.objects.create(
                name=f"Signature Product {i}",
                slug=f"signature-product-{i}",
                sku=f"pc-{cat}-pp-{i}",
                description=f"This is the description for Signature Product {i}. It is crafted with excellence and designed to fit perfectly into your daily life.",
                # price=Decimal(str(random.randint(49, 299))) + Decimal("0.99"),
                # category=cat,
                is_active=True,
            )
            products.append(prod)

            # Note: Because we are using remote URLs instead of local files,
            # we are writing the URL string directly into the CharField/ImageField.
            # In your probo UI, you just use `p.get('image')` and it will render the URL.

            # Main product image
            if hasattr(prod, "image"):
                prod.image = get_random_image_url(seed=f"prod_{prod.id}")
                prod.save()

            # Create 1-3 extra gallery images

        # 3. Create 200 Variants (10 per Product)
        self.stdout.write("Creating 200 Product Variants...")
        sizes = ["S", "M", "L", "XL", "XXL"]
        colors = ["Black", "White", "Navy", "Crimson", "Olive", "Charcoal", "Ivory"]

        variant_count = 0
        for prod in products:
            for v in range(1, 11):
                # 80% chance to be active, 20% chance to be deactivated
                is_active = random.random() > 0.20

                variant = ProductVariant.objects.create(
                    product=prod,
                    sku=f"SKU-{prod.id}-V{v}-VC-{variant_count}-NM-{i}",
                    slug=f"{prod.slug}-V{v}-VC-{variant_count}-NM-{i}",
                    promo_price=Decimal(str(random.choice([0.00, 5.00, 10.00, -5.00]))),
                    base_price=Decimal(str(0.5 * random.choice([0.00, 5.00, 10.00, -5.00]))),
                    stock=random.randint(0, 100) if is_active else 0,
                    is_active=is_active,
                    size=random.choice(sizes),
                    color=random.choice(colors),
                )

                variant.save()
                variant_count += 1

                for j in range(random.randint(1, 3)):
                    ProductImage.objects.create(
                        variant=variant,
                        # We use a string path that your UI will read.
                        # If ProductImage.image requires a File object, this might fail,
                        # but typically CharField/ImageFields accept string paths.
                        image=get_random_image_url(seed=f"gallery_{prod.id}_{j}"),
                        alt_text=f"Gallery image {j} for {prod.name}",
                        is_primary=True if j == 1 else False,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created 20 Categories, 20 Products, and {variant_count} Variants with remote images!"
            )
        )
