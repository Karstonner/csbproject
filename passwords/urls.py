from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password/<int:id>/', views.password_detail, name='password_detail'),
    path('delete/<int:id>/', views.password_delete, name='password_delete'),
    path('search/', views.search_passwords, name='search_passwords'),
    path('create/', views.password_create, name='password_create'),
    path('edit/<int:id>/', views.password_edit, name='password_edit'),
    path('generate/', views.generate_password, name='generate_password'),
    path('fetch_favicon/<int:id>', views.fetch_favicon, name='fetch_favicon'),
    path('logout/', views.custom_logout, name='logout'),
]
