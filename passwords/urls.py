from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password/<int:id>/', views.password_detail, name='password_detail'),
    path('delete/<int:id>/', views.password_delete, name='password_delete'),
    path('search/', views.search_passwords, name='search_passwords'),
]