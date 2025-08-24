from django.db import models
from django.contrib.auth.models import User
import base64

def encrypt_password(password):
    return base64.b64encode(password.encode()).decode()

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100)
    site_url = models.URLField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.password = encrypt_password(self.password) # Weak encoding with Base64
        super().save(*args, **kwargs)
    
    def decrypted_password(self):
        return base64.b64decode(self.password.encode()).decode()