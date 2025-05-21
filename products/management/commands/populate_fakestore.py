# products/management/commands/populate_fakestore.py

import requests
from django.core.management.base import BaseCommand
from accounts.models import Product
from django.core.files.base import ContentFile
from uuid import uuid4
from decimal import Decimal
from category.models import ProductCategory

class Command(BaseCommand):
    help = 'Populate the Product table using data from fakestoreapi.com'

    def handle(self, *args, **kwargs):
        url = 'https://fakestoreapi.com/products/'
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch data'))
            return

        data = response.json()
        added = 0
        
        for item in data:
            title = item['title']
            

            if Product.objects.filter(name=title).exists():
                continue
            category_name = item['category']
            category_obj = ProductCategory.objects.filter(name__iexact=category_name).first()

            product = Product(
                name=title,
                description=item['description'][:500],
                quantity=100,
                price=Decimal(item['price']),
                discount_price=Decimal(item['price']) * Decimal('0.9'),
                is_published=True,
                currency='USD',
                size='M',
                colours='Black',
                category=category_obj
            )

            # Download and save image
            image_url = item['image']
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                product.image.save(f"{uuid4()}.jpg", ContentFile(image_response.content), save=True)
                product.save()
                added += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {product.name}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Total products added: {added}"))
