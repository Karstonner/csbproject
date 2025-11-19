from django.db import models
from django.contrib.auth.models import User
import base64
# FIX: Import a secure encryption library
# from cryptography.fernet import Fernet

def encrypt_password(password):
    # FIX: Use a secure encryption method (e.g., Fernet with a securely stored key)
    # key = Fernet.generate_key() # Generate key securely and store it safely
    # fernet = Fernet(key)
    # return fernet.encrypt(password.encode()).decode()
    return base64.b64encode(password.encode()).decode()

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_passwords')
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_passwords') 
    site_name = models.CharField(max_length=100)
    site_url = models.URLField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        try:
            decoded = base64.b64decode(self.password.encode()).decode()
        except Exception:
            self.password = encrypt_password(self.password) # Weak encoding with Base64 (A02)
        super().save(*args, **kwargs)
    
    def decrypted_password(self):
        # FIX: Use corresponding decryption method
        # fernet = Fernet(key) # Load the same key used for encryption
        # return fernet.decrypt(self.password.encode()).decode()
        return base64.b64decode(self.password.encode()).decode()
