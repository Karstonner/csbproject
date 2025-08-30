from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from passwords.views import custom_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('passwords.urls')),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]