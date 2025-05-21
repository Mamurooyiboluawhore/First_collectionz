# category/management/commands/populate_categories.py

import requests
from django.core.management.base import BaseCommand
from category.models import ProductCategory

class Command(BaseCommand):
    help = 'Populate the ProductCategory table using data from fakestoreapi.com'

    def handle(self, *args, **kwargs):
        url = 'https://fakestoreapi.com/products/categories'
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch category data'))
            return

        categories = response.json()
        added = 0

        for name in categories:
            if not ProductCategory.objects.filter(name__iexact=name).exists():
                ProductCategory.objects.create(name=name)
                added += 1
                self.stdout.write(self.style.SUCCESS(f"Added category: {name}"))
            else:
                self.stdout.write(f"Skipped (already exists): {name}")

        self.stdout.write(self.style.SUCCESS(f"✅ Total categories added: {added}"))
import logging

logger = logging.getLogger(__name__)

...

def handle(self, *args, **kwargs):
    logger.info('Starting to populate categories')
    url = 'https://fakestoreapi.com/products/categories'
    response = requests.get(url)

    if response.status_code != 200:
        logger.error('Failed to fetch category data')
        self.stdout.write(self.style.ERROR('Failed to fetch category data'))
        return

    categories = response.json()
    added = 0

    for name in categories:
        if not ProductCategory.objects.filter(name__iexact=name).exists():
            ProductCategory.objects.create(name=name)
            added += 1
            logger.info(f"Added category: {name}")
            self.stdout.write(self.style.SUCCESS(f"Added category: {name}"))
        else:
            logger.info(f"Skipped (already exists): {name}")
            self.stdout.write(f"Skipped (already exists): {name}")

    logger.info(f"✅ Total categories added: {added}")
    self.stdout.write(self.style.SUCCESS(f"✅ Total categories added: {added}"))