from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from users.models import CustomUser
from shops.models import Shop
from categories.models import Category
from products.models import Product


class Command(BaseCommand):
    help = "Seed the marketplace with demo sellers, shops, categories and products."

    SELLERS = [
        {
            "folder": "seller1",
            "username": "moro_planet",
            "email": "moro@example.com",
            "password": "Seller12345!",
            "shop_name": "Moro Planet",
            "description": "A handmade accessories shop offering stylish personalised pieces, watches and car accessories.",
            "address": "Damascus, Syria",
            "phone": "0991000001",
            "categories": [
                "Car Accessories",
                "Necklaces",
                "Watches",
            ],
            "product_names": [
                "Personalised Car Charm",
                "Elegant Car Hanging",
                "Name Necklace",
                "Classic Necklace",
                "Women's Watch",
                "Men's Watch",
                "Soft Strap Watch",
                "Personalised Pendant",
                "Decorative Accessory",
            ],
            "prices": [
                45000,
                55000,
                60000,
                65000,
                85000,
                95000,
                75000,
                50000,
                40000,
            ],
        },
        {
            "folder": "seller2",
            "username": "reem_candles",
            "email": "reem@example.com",
            "password": "Seller12345!",
            "shop_name": "Reem Candles",
            "description": "Handcrafted candles designed for gifts, celebrations and beautiful home decoration.",
            "address": "Damascus, Syria",
            "phone": "0991000002",
            "categories": [
                "Gift Candles",
                "Favor Candles",
                "Scented Candles",
            ],
            "product_names": [
                "Elegant Scented Candle",
                "Large Rose Gift Candle",
                "Personalised Name Candle",
                "Rose Gift Candle",
                "Sunflower Candle",
                "Colourful Flower Candle",
                "Special Occasion Candle",
                "Decorative Floral Candle",
            ],
            "prices": [
                35000,
                70000,
                50000,
                55000,
                45000,
                50000,
                40000,
                60000,
            ],
        },
        {
            "folder": "seller3",
            "username": "semak_handmade",
            "email": "semak@example.com",
            "password": "Seller12345!",
            "shop_name": "Semak Handmade",
            "description": "Creative handmade pieces made with care, combining decorative details with unique gift ideas.",
            "address": "Damascus, Syria",
            "phone": "0991000003",
            "categories": [
                "Handmade Gifts",
                "Home Decor",
                "Accessories",
            ],
            "product_names": [
                "Handmade Gift Piece",
                "Decorative Handmade Piece",
                "Artisan Gift",
                "Handcrafted Decoration",
                "Special Handmade Gift",
                "Decorative Accessory",
                "Creative Handmade Piece",
                "Elegant Handmade Gift",
                "Artisan Decoration",
                "Handcrafted Accessory",
                "Unique Gift Piece",
                "Decorative Craft",
                "Premium Handmade Piece",
                "Modern Handmade Decor",
                "Creative Gift",
                "Artisan Accessory",
                "Handmade Collection Piece",
                "Special Decorative Piece",
                "Handcrafted Gift",
                "Unique Handmade Decor",
                "Elegant Craft Piece",
            ],
            "prices": [
                35000, 40000, 45000, 50000, 55000,
                60000, 45000, 50000, 65000, 40000,
                55000, 60000, 70000, 50000, 45000,
                65000, 55000, 60000, 75000, 50000,
                65000,
            ],
        },
        {
            "folder": "seller4",
            "username": "sandra_wood",
            "email": "sandra@example.com",
            "password": "Seller12345!",
            "shop_name": "Sandra Wood",
            "description": "Handcrafted wooden products and decorative pieces designed for homes, gifts and special occasions.",
            "address": "Damascus, Syria",
            "phone": "0991000004",
            "categories": [
                "Wooden Gifts",
                "Home Decor",
                "Wood Accessories",
            ],
            "product_names": [
                "Handmade Wooden Gift",
                "Wooden Decorative Piece",
                "Elegant Wood Decor",
                "Personalised Wooden Gift",
                "Wooden Home Accessory",
                "Decorative Wood Art",
                "Handcrafted Wooden Piece",
                "Rustic Home Decoration",
                "Wooden Gift Design",
                "Modern Wood Decoration",
                "Artisan Wooden Piece",
                "Decorative Wooden Accessory",
                "Special Wooden Gift",
                "Handmade Wood Art",
                "Premium Wooden Decoration",
                "Creative Wooden Piece",
            ],
            "prices": [
                60000, 75000, 80000, 90000,
                55000, 70000, 85000, 95000,
                65000, 75000, 100000, 60000,
                85000, 90000, 110000, 70000,
            ],
        },
        {
            "folder": "seller5",
            "username": "hiba_flowers",
            "email": "hiba@example.com",
            "password": "Seller12345!",
            "shop_name": "Hiba Flowers",
            "description": "Beautiful floral arrangements and handcrafted bouquets created for gifts, celebrations and memorable moments.",
            "address": "Damascus, Syria",
            "phone": "0991000005",
            "categories": [
                "Flower Bouquets",
                "Gift Arrangements",
                "Decorative Flowers",
            ],
            "product_names": [
                "Elegant Flower Bouquet",
                "Romantic Flower Arrangement",
                "Special Gift Bouquet",
                "Classic Floral Bouquet",
                "Luxury Flower Arrangement",
                "Decorative Flower Design",
                "Celebration Bouquet",
                "Handcrafted Floral Gift",
                "Premium Flower Bouquet",
                "Colourful Flower Arrangement",
                "Elegant Gift Flowers",
                "Modern Floral Design",
                "Special Occasion Bouquet",
                "Decorative Floral Arrangement",
                "Luxury Gift Flowers",
                "Beautiful Flower Bouquet",
                "Premium Floral Gift",
            ],
            "prices": [
                75000, 85000, 90000, 70000,
                120000, 80000, 95000, 85000,
                130000, 75000, 100000, 90000,
                110000, 85000, 140000, 95000,
                120000,
            ],
        },
    ]

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

    def handle(self, *args, **options):
        project_root = Path(__file__).resolve().parents[3]
        seed_root = project_root / "seed_images"

        if not seed_root.exists():
            self.stderr.write(
                self.style.ERROR(
                    f"seed_images folder was not found at: {seed_root}"
                )
            )
            return

        self.stdout.write(
            self.style.WARNING("Starting marketplace seed...")
        )

        with transaction.atomic():
            for seller_data in self.SELLERS:
                self.seed_seller(seed_root, seller_data)

        self.stdout.write(
            self.style.SUCCESS(
                "Marketplace seeded successfully."
            )
        )

    def seed_seller(self, seed_root, data):
        # --------------------------------
        # Seller account
        # --------------------------------

        seller, created = CustomUser.objects.get_or_create(
            username=data["username"],
            defaults={
                "email": data["email"],
                "role": "seller",
                "phone_number": data["phone"],
                "location": data["address"],
            },
        )

        if created:
            seller.set_password(data["password"])
            seller.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created seller: {seller.username}'
                )
            )
        else:
            # Make sure existing seed account is still a seller.
            changed = False

            if seller.role != "seller":
                seller.role = "seller"
                changed = True

            if not seller.email:
                seller.email = data["email"]
                changed = True

            if changed:
                seller.save()

            self.stdout.write(
                f'Seller already exists: {seller.username}'
            )

        # --------------------------------
        # Shop
        # --------------------------------

        shop, shop_created = Shop.objects.get_or_create(
            owner=seller,
            defaults={
                "shopName": data["shop_name"],
                "shopDescription": data["description"],
                "shopAddress": data["address"],
                "shopNumber": data["phone"],
                "shopEmail": data["email"],
            },
        )

        if shop_created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created shop: {shop.shopName}'
                )
            )

        # --------------------------------
        # Categories
        # --------------------------------

        categories = []

        for category_name in data["categories"]:
            category, _ = Category.objects.get_or_create(
                name=category_name,
                seller=seller,
            )

            categories.append(category)

        # --------------------------------
        # Images
        # --------------------------------

        seller_folder = seed_root / data["folder"]

        if not seller_folder.exists():
            self.stderr.write(
                self.style.WARNING(
                    f'Skipping {data["folder"]}: folder not found.'
                )
            )
            return

        image_files = sorted(
            [
                file
                for file in seller_folder.iterdir()
                if file.is_file()
                and file.suffix.lower() in self.IMAGE_EXTENSIONS
                and file.name != ".gitkeep"
            ],
            key=lambda path: path.name.lower(),
        )

        if not image_files:
            self.stderr.write(
                self.style.WARNING(
                    f'No images found inside {data["folder"]}.'
                )
            )
            return

        self.stdout.write(
            f'{shop.shopName}: found {len(image_files)} images.'
        )

        # --------------------------------
        # Products
        # --------------------------------

        for index, image_path in enumerate(image_files):
            product_number = index + 1

            if index < len(data["product_names"]):
                product_name = data["product_names"][index]
            else:
                product_name = (
                    f'{data["shop_name"]} Product {product_number}'
                )

            if index < len(data["prices"]):
                price = data["prices"][index]
            else:
                price = 50000 + (index * 5000)

            category = categories[index % len(categories)]

            description = (
                f"A carefully selected product from "
                f"{data['shop_name']}. "
                f"This item belongs to the {category.name} collection "
                f"and is suitable for gifts, personal use, or special occasions. "
                f"Handpicked to showcase the unique style of the shop."
            )

            product, product_created = Product.objects.get_or_create(
                productName=product_name,
                shop=shop,
                defaults={
                    "productPrice": price,
                    "productDescription": description,
                    "category": category,
                },
            )

            if not product_created:
                self.stdout.write(
                    f'Product already exists: {product_name}'
                )
                continue

            # Saving through Django's configured storage backend.
            # On Render this will be Cloudinary.
            try:
                with image_path.open("rb") as image_file:
                    product.productImage.save(
                        image_path.name,
                        File(image_file),
                        save=True,
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created product: {product_name} '
                        f'- {price:,} SYP'
                    )
                )

            except Exception as error:
                # Delete incomplete product if image upload failed.
                product.delete()

                self.stderr.write(
                    self.style.ERROR(
                        f'Failed to upload {image_path.name}: {error}'
                    )
                )
