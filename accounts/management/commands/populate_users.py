# accounts/management/commands/populate_users.py

import requests
from django.core.management.base import BaseCommand
from accounts.models import User
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'Populate the User table using data from fakestoreapi.com'

    def handle(self, *args, **kwargs):
        url = 'https://fakestoreapi.com/users'
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch user data'))
            return

        users = response.json()
        added = 0

        for user_data in users:
            email = user_data['email']
            full_name = f"{user_data['name']['firstname']} {user_data['name']['lastname']}"

            if User.objects.filter(email=email).exists():
                continue

            password = get_random_string(8)  # Or use a fixed default password

            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
            )

            added += 1
            self.stdout.write(self.style.SUCCESS(f"✅ Created user: {email}"))

        self.stdout.write(self.style.SUCCESS(f"🎉 Total users added: {added}"))
