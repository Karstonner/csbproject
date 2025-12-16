from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken

FERNET_KEY = getattr(settings, 'FERNET_KEY', None)
if FERNET_KEY is None:
    raise RuntimeError("FERNET_KEY is not set in Django settings")

fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_passwords')
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_passwords') 
    site_name = models.CharField(max_length=100)
    site_url = models.URLField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        try:
            fernet.decrypt(self.password.encode())
        except (InvalidToken, Exception):
            self.password = encrypt_password(self.password)
        super().save(*args, **kwargs)
    
    def decrypted_password(self):
        try:
            return fernet.decrypt(self.password.encode()).decode()
        except InvalidToken:
            return None
        