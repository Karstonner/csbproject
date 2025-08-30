from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from passwords.views import custom_login, custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('passwords.urls')),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
]