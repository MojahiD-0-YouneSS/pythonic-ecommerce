import os
import random
import uuid
import urllib.request
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files import File
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
from django.template.defaultfilters import slugify

from apps.product.models import Product, ProductVariant, Category, ProductImage
from apps.client.models import Client, ClientProfile
from apps.order.models import Order, OrderItem, BillingAddress, ShippingAddress
from apps.cms.models import Banner, Testimony

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the database with 20 realistic products, 400 variants, clients, orders, and CMS data."

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            action='store_true',
            help='Format the database (delete existing mock data) before seeding.',
        )

    def handle(self, *args, **options):
        format_db = options['format']

        if format_db:
            self.stdout.write(self.style.WARNING('Formatting database (deleting existing data)...'))
            Product.objects.all().delete()
            ProductVariant.objects.all().delete()
            Category.objects.all().delete()
            Client.objects.all().delete()
            Order.objects.all().delete()
            Banner.objects.all().delete()
            Testimony.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Database formatted.'))

        # 0. Always ensure admins exist
        su_username = 'qwertyuiop'
        if not User.objects.filter(username=su_username).exists():
            User.objects.create_superuser(username=su_username, email='su@example.com', password='asdfghjkl;@&')
            self.stdout.write(self.style.SUCCESS(f'Created Superuser: {su_username}'))
        
        store_manager_group, _ = Group.objects.get_or_create(name='store_manager')
        admin_username = 'admin_1'
        if not User.objects.filter(username=admin_username).exists():
            admin_user = User.objects.create_user(username=admin_username, email='admin1@example.com', password='.0123654789')
            admin_user.groups.add(store_manager_group)
            self.stdout.write(self.style.SUCCESS(f'Created User: {admin_username} and added to store_manager group'))

        self.stdout.write('Seeding Clients with human data...')
        first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        
        clients = []
        for i in range(10):
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            unique_uid = uuid.uuid4().hex[:6]
            username = f"{fname.lower()}_{lname.lower()}_{unique_uid}"
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f"{username}@example.com",
                    'first_name': fname,
                    'last_name': lname
                }
            )
            if created:
                user.set_password("password123")
                user.save()
                
            session_key = str(uuid.uuid4())
            client, _ = Client.objects.get_or_create(
                user=user,
                defaults={
                    'session_key': session_key,
                    'phone_number': f"+1{random.randint(2000000000, 9999999999)}",
                    'nickname': f"{fname}{unique_uid}",
                    'address': f"{random.randint(100, 9999)} {random.choice(['Oak', 'Maple', 'Cedar', 'Elm', 'Pine'])} Street, NY, USA"
                }
            )
            ClientProfile.objects.get_or_create(
                session_key=client.session_key,
                defaults={'status': ClientProfile.ClientStatus.ACTIVE}
            )
            clients.append(client)

        # 2. Create Categories
        self.stdout.write('Seeding Categories...')
        cat_names = ["Electronics", "Apparel", "Home & Garden", "Sports & Outdoors", "Health & Beauty", "Footwear"]
        categories = []
        for name in cat_names:
            try:
                cat, _ = Category.objects.get_or_create(
                    name=name,
                    defaults={
                        'description': f"Browse our collection of premium {name.lower()}.",
                        'slug': slugify(name)
                    }
                )
            except Exception:
                unique_uid = uuid.uuid4().hex[:4]
                unique_name = f"{name}_{unique_uid}"
                cat, _ = Category.objects.get_or_create(
                    name=unique_name,
                    defaults={
                        'description': f"Browse our collection of premium {name.lower()}.",
                        'slug': slugify(unique_name)
                    }
                )
            categories.append(cat)

        # 3. Create Products & Variants
        self.stdout.write('Seeding Products and Variants (Generating Images for ALL variants)...')
        realistic_products = [
            ("Men's Classic Cotton T-Shirt", "A comfortable, breathable everyday tee."),
            ("Wireless Noise-Cancelling Headphones", "Premium sound quality with active noise cancellation."),
            ("Stainless Steel Insulated Water Bottle", "Keeps drinks cold for 24 hours or hot for 12 hours."),
            ("Professional Yoga Mat", "Non-slip, extra thick mat for all types of yoga and pilates."),
            ("Smart Fitness Tracker Watch", "Monitor your heart rate, sleep, and daily activities."),
            ("Organic Cotton Bed Sheets", "Luxurious 400-thread count sheets for a perfect night's sleep."),
            ("Ceramic Coffee Mug Set", "Handcrafted minimalist mugs, perfect for your morning brew."),
            ("Ergonomic Office Chair", "Adjustable lumbar support for long working hours."),
            ("Leather Crossbody Bag", "Elegant, durable, and spacious enough for your essentials."),
            ("Minimalist Desk Lamp", "Adjustable LED lamp with 3 color temperatures."),
            ("Polarized Vintage Sunglasses", "UV400 protection with a classic retro design."),
            ("Ultra-Cushion Running Shoes", "Engineered for marathon runners and casual joggers alike."),
            ("Acoustic Guitar", "Beginner-friendly dreadnought guitar with rich resonance."),
            ("Digital SLR Camera", "Capture stunning 4K videos and 24MP photos."),
            ("Bluetooth Portable Speaker", "Waterproof rugged speaker with 20h battery life."),
            ("Gourmet Espresso Beans", "Dark roast whole beans sourced from Colombia."),
            ("Scented Lavender Soy Candle", "Hand-poured candle with a relaxing 40-hour burn time."),
            ("Skincare Travel Kit", "TSA-approved set including cleanser, toner, and moisturizer."),
            ("Waterproof Hiking Boots", "Durable all-terrain boots designed for maximum traction."),
            ("Canvas Laptop Backpack", "Water-resistant commuter bag with padded compartments.")
        ]

        products = []
        colors = ["Black", "White", "Navy", "Grey", "Red"]
        sizes = ["Small", "Medium", "Large", "Extra Large"]

        for idx, (prod_name, prod_desc) in enumerate(realistic_products):
            unique_suffix = uuid.uuid4().hex[:4].upper()
            prod_name_unique = f"{prod_name} {unique_suffix}"
            
            prod = Product.objects.create(
                reference_number=f"P-{unique_suffix}{idx}",
                name=prod_name_unique,
                description=prod_desc,
                short_description=prod_desc[:50] + "...",
                sku=f"SKU-{idx:03d}-{unique_suffix}",
                is_featured=(idx % 3 == 0)
            )
            prod.categories.add(random.choice(categories))
            if random.random() > 0.5:
                prod.categories.add(random.choice(categories))
            
            products.append(prod)

            for color in colors:
                for size in sizes:
                    var_uuid = uuid.uuid4().hex[:4].upper()
                    var_sku = f"SKU-{idx:03d}-{color[:3].upper()}-{size[:1]}-{var_uuid}"
                    variant = ProductVariant.objects.create(
                        reference_number=f"V-{uuid.uuid4().hex[:6].upper()}",
                        product=prod,
                        sku=var_sku,
                        size=size,
                        color=color,
                        stock=random.randint(10, 150),
                        base_price=Decimal(random.randint(20, 299)) + Decimal('0.99'),
                        promo_price=Decimal(random.randint(15, 250)) + Decimal('0.99'),
                    )

                    # Guaranteed External Image URL using context
                    keyword = ''.join(filter(str.isalpha, prod_name.split()[-1].lower()))
                    p_img = ProductImage.objects.create(
                        variant=variant,
                        image=f"https://loremflickr.com/800/800/{keyword},{color.lower()}?lock={random.randint(1, 1000)}",
                        alt_text=f"{prod_name} in {color}",
                        is_primary=True
                    )

        # 4. Create Orders
        self.stdout.write('Seeding Orders...')
        for client in clients:
            bill = BillingAddress.objects.create(
                session_key=client.session_key,
                full_name=client.user.username,
                address_line_1=client.address,
                city="New York",
                state="NY",
                postal_code="10001",
                country="USA",
                phone_number=client.phone_number
            )
            ship = ShippingAddress.objects.create(
                session_key=client.session_key,
                full_name=client.user.username,
                address_line_1=client.address,
                city="New York",
                state="NY",
                postal_code="10001",
                country="USA",
                phone_number=client.phone_number
            )
            order = Order.objects.create(
                session_key=client.session_key,
                billing_address=bill,
                shipping_address=ship,
                total_amount=Decimal(0),
                status=random.choice(['Pending', 'Processing', 'Shipped', 'Delivered'])
            )
            
            total = Decimal(0)
            for _ in range(random.randint(1, 4)):
                variant = ProductVariant.objects.order_by('?').first()
                qty = random.randint(1, 3)
                price = variant.base_price
                OrderItem.objects.create(
                    order=order,
                    product_variant=variant,
                    quantity=qty,
                    price=price
                )
                total += (price * qty)
            
            order.total_amount = total
            order.save()

        # 5. Create CMS Data
        self.stdout.write('Seeding CMS Data (Banners & Testimonies)...')
        promos = ["Summer Sale Event", "New Arrivals Are Here", "Clearance Blowout"]
        for i, promo in enumerate(promos):
            Banner.objects.create(
                title=f"{promo} {uuid.uuid4().hex[:4]}",
                subtitle="Exclusive deals for a limited time.",
                image=f"https://picsum.photos/seed/{uuid.uuid4().hex[:6]}/1200/400",
                position=i+1,
                is_featured=True
            )

        feedbacks = [
            "Absolutely amazing! Exceeded all my expectations. Will buy again.",
            "Great quality, fast shipping, and exactly as described.",
            "Customer service was fantastic and the product is phenomenal.",
            "I've recommended this to all my friends. Truly 5 stars.",
            "A must-buy. The material feels premium and it looks great."
        ]

        for i in range(5):
            gender = random.choice(['men', 'women'])
            img_id = random.randint(1, 99)
            Testimony.objects.create(
                customer_name=clients[i].user.get_full_name() or clients[i].nickname,
                customer_image=f"https://randomuser.me/api/portraits/{gender}/{img_id}.jpg",
                feedback=feedbacks[i],
                rating=5,
                product=products[i],
                is_approved=True,
                highlighted=True
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with humanized data and complete images!'))
