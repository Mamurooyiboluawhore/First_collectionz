from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drop the product_id column from the promotion table'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('ALTER TABLE "accounts_chatmessages" DROP COLUMN IF EXISTS user_id;')
        self.stdout.write(self.style.SUCCESS("Successfully dropped 'product_review' column from 'promotion' table"))

