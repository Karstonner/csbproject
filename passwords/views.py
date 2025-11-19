from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PasswordEntry
from .forms import PasswordEntryForm, LoginForm
import requests
import time
import logging

logger = logging.getLogger('django')

def dashboard(request):
    # Broken Access Control (A01): Show owned and shared passwords without checks
    # FIX: Filter passwords to ensure only owned or shared passwords are accessible
    # passwords = PasswordEntry.objects.filter(user=request.user).union(PasswordEntry.objects.filter(shared_with=request.user)).distinct()
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        owned_passwords = PasswordEntry.objects.none()
        shared_passwords = PasswordEntry.objects.none()
    else:
        user = request.user
        owned_passwords = PasswordEntry.objects.filter(user=user)
        shared_passwords = PasswordEntry.objects.filter(shared_with=user)
    
    return render(request, 'passwords/dashboard.html', {
        'passwords': owned_passwords | shared_passwords
    })

def password_detail(request, id):
    # Broken Access Control (A01): No ownership check
    # FIX: Verify the user owns or has shared access to the password entry
    # password = get_object_or_404(PasswordEntry, id=id, user=request.user) | get_object_or_404(PasswordEntry, id=id, shared_with=request.user)
    password = get_object_or_404(PasswordEntry, id=id)
    password.decrypted = password.decrypted_password() # Cryptographic failure (A02)
    return render(request, 'passwords/password_detail.html', {'password': password})

def password_delete(request, id):
    # Broken Access Control (A01): No ownership check
    # FIX: Restrict deletion to the owner of the password entry
    # password = get_object_or_404(PasswordEntry, id=id, user=request.user)
    # FIX: Log unauthorized access attempts
    # if password.user != request.user:
    #     logger.warning(f"Unauthorized delete attempt by {request.user.username} on PasswordEntry {id}")
    password = get_object_or_404(PasswordEntry, id=id)
    password.delete()
    return redirect('dashboard')

def search_passwords(request):
    # Injection (A03): Raw SQL query
    # FIX: Use Django ORM or parameterer queries
    # results = PaswordEntry.objects.filter(site_name__icontains=query)
    query = request.GET.get('q', '')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM passwords_passwordentry WHERE site_name LIKE '%{query}%'")
        results = cursor.fetchall()
    return render(request, 'passwords/search_results.html', {'results': results})

@csrf_exempt
@login_required
def password_create(request):
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            password_entry = form.save(commit=False)
            password_entry.user = request.user
            password_entry.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = PasswordEntryForm()
    return render(request, 'passwords/password_form.html', {'form': form})

@csrf_exempt
@login_required
def password_edit(request, id):
    # Broken Access Control (A01): No ownership check
    # FIX: Restrict editing to the owner of the password entry
    # password = get_object_or_404(PasswordEntry, id=id, user=request.user)
    # FIX: Log unauthorized access attempts
    # if password.user != request.user:
    #     logger.warning(f"Unauthorized edit attempt by {request.user.username} on PasswordEntry {id}")
    password = get_object_or_404(PasswordEntry, id=id)
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, instance=password)
        if form.is_valid():
            form.save() # Updates without checking ownership
            return redirect('dashboard')
    else:
        form = PasswordEntryForm(instance=password)
    return render(request, 'passwords/password_form.html', {'form': form})

def fetch_favicon(request, id):
    # SSRF (A10): No URL validation, including file://
    # FIX: Validate URLs to allow only specific safe domains
    # from urllib.parse import urlparse
    # allowed_domains = ['example.com', 'www.example.com']
    # parsed_url = urlparse(url)
    # if parsed_url.scheme not in ['http', 'https'] or parsed_url.netloc not in allowed_domains:
    #     raise ValueError("Invalid or unauthorized URL")
    # Broken Access Control (A01): No ownership check
    # FIX: Ensure user owns or has shared access to the password entry
    # password = get_object_or_404(PasswordEntry, id=id, user=request.user) | get_object_or_404(PasswordEntry, id=id, shared_with=request.user)
    password = get_object_or_404(PasswordEntry, id=id)
    url = request.GET.get('url', password.site_url)
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        return HttpResponse(response.content, content_type='text/plain')
    except requests.RequestException:
        return HttpResponse("Failed to fetch URL", status=500)

def generate_password(request):
    # Cryptographic Failures (A02): Weak, predictable passwords
    # FIX: Use a cryptographically secure random generator
    # import secrets
    # weak_password = secrets.token_urlsafe(16) # Generate a secure, random password
    seed = str(int(time.time())) # Predictable seed
    weak_password = seed[-8:]
    return render(request, 'passwords/generate_password.html', {'generated_password': weak_password})

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                logger.info(f"User {user.username} logged in successfully")
                return redirect('dashboard')
            else:
                # No logging of failed attempts (A09)
                # FIX: Log failed login attempts for monitoring
                # logger.warning(f"Failed login attempt for username: {username}")
                return render(request, 'passwords/login.html', {'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'passwords/login.html', {'form': form})

@csrf_exempt
def custom_logout(request):
    logout(request)
    return redirect('login')