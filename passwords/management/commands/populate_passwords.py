from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from passwords.models import PasswordEntry

class Command(BaseCommand):
    help = 'Populates the database with dummy password entries'

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(username='testuser', defaults={'password': 'test123'})
        for i in range(5):
            # FIX: Encrypt passwords using a secure method before saving
            # PasswordEntry.objects.create(..., password=encrypt_password(f'password{i}'))
            PasswordEntry.objects.create(
                user=user,
                site_name=f'Site {i}',
                site_url=f'http://example{i}.com',
                username=f'user{i}',
                password=f'password{i}'
            )
        self.stdout.write(self.style.SUCCESS('Successfully populated 5 password entries'))
