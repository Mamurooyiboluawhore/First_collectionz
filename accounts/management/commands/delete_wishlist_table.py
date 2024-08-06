from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Delete the wishlist table from the database'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS accounts_chatmessages;")
        self.stdout.write(self.style.SUCCESS("Successfully deleted 'wishlist' table"))
