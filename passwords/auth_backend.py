from django.contrib.auth.models import User

class InsecureAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username) # Case insensitive
            if user.password == password: # Plaintext
                return user
            return None
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None