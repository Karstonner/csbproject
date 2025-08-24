from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import PasswordEntry

def dashboard(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    return render(request, 'passwords/dashboard.html', {'passwords': passwords})

def password_detail(request, id):
    # Broken Access Control (A01): No ownership check
    password = get_object_or_404(PasswordEntry, id=id)
    password.decrypted = password.decrypted_password() # Cryptographic failure (A02)
    return render(request, 'passwords/password_detail.html', {'password': password})

def password_delete(request, id):
    # Broken Access Control (A01): No ownership check
    password = get_object_or_404(PasswordEntry, id=id)
    password.delete()
    return redirect('dashboard')

def search_passwords(request):
    # Injection (A03): Raw SQL query
    query = request.GET.get('q', '')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM passwords_passwordentry WHERE site_name LIKE '%{query}%'")
        results = cursor.fetchall()
    return render(request, 'passwords/search_results.html', {'results': results})
