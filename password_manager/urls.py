from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from passwords.views import custom_login, custom_logout, dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('', include('passwords.urls'), name='passwords'),
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),
    # path('logout/', custom_logout, name='logout'),
]