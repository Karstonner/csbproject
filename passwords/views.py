from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import PasswordEntry
from .forms import PasswordEntryForm, LoginForm
from urllib.parse import urlparse
import requests
import logging
import secrets

logger = logging.getLogger('django')

def dashboard(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        passwords = PasswordEntry.objects.none()
    else:
        user = request.user
        passwords = PasswordEntry.objects.filter(user=user).union(PasswordEntry.objects.filter(shared_with=user))
    
    return render(request, 'passwords/dashboard.html', {
        'passwords': passwords
    })

@login_required
def password_detail(request, id):
    password = get_object_or_404(PasswordEntry, Q(id=id) & (Q(user=request.user) | Q(shared_with=request.user)))
    password.decrypted = password.decrypted_password()
    return render(request, 'passwords/password_detail.html', {'password': password})

@login_required
def password_delete(request, id):
    password = get_object_or_404(PasswordEntry, id=id, user=request.user)
    if password.user != request.user:
        logger.warning(f"Unauthorized delete attempt by {request.user.username} on PasswordEntry {id}")
    password.delete()
    return redirect('dashboard')

@login_required
@require_POST
def password_reveal(request, id):
    confirm_password = request.POST.get('confirm_password', '')
    user = request.user
    if not authenticate(username=user.username, password=confirm_password):
        return HttpResponseForbidden("Re-authentication failed")
    password = get_object_or_404(PasswordEntry, Q(id=id) & (Q(user=user) | Q(shared_with=user)))
    decrypted = password.decrypted_password()
    if decrypted is None:
        return JsonResponse({'error': 'decryption_failed'}, status=500)
    return JsonResponse({'password': decrypted})

@login_required
def search_passwords(request):
    query = request.GET.get('q', '')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM passwords_passwordentry WHERE site_name LIKE '%{query}%'")
        results = PasswordEntry.objects.filter(site_name__icontains=query)
    return render(request, 'passwords/search_results.html', {'results': results})

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

@login_required
def password_edit(request, id):
    password = get_object_or_404(PasswordEntry, id=id, user=request.user)
    if password.user != request.user:
        logger.warning(f"Unauthorized edit attempt by {request.user.username} on PasswordEntry {id}")
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, instance=password)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PasswordEntryForm(instance=password)
    return render(request, 'passwords/password_form.html', {'form': form})

@login_required
def fetch_favicon(request, id):
    password = get_object_or_404(PasswordEntry, Q(id=id) & (Q(user=request.user) | Q(shared_with=request.user)))
    url = request.GET.get('url', password.site_url)
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return HttpResponse("Invalid URL", status=400)
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        content_type = response.headers.get("Content-Type", "application/octet-stream")
        return HttpResponse(response.content, content_type=content_type)
    except requests.RequestException:
        return HttpResponse("Failed to fetch URL", status=500)

def generate_password(request):
    weak_password = secrets.token_urlsafe(16)
    return render(request, 'passwords/generate_password.html', {'generated_password': weak_password})

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
                logger.warning(f"Failed login attempt for username: {user.username}")
                return render(request, 'passwords/login.html', {'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'passwords/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')