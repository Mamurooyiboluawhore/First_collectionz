from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Delete the initial migration for the cart app from the migration history'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations WHERE app = 'cart' AND name = '0001_initial';")
        self.stdout.write(self.style.SUCCESS("Successfully deleted 'cart.0001_initial' migration from history"))
