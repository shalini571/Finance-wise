# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User

@ensure_csrf_cookie
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully')
        login(request, user)
        return redirect('home')

    return render(request, 'authentication/register.html')

def validate_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', '')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username is already taken'})
        return JsonResponse({'username_valid': True})

def validate_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email', '')
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is already registered'})
        return JsonResponse({'email_valid': True})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            if '@' in username:
                user = User.objects.get(email=username)
                username = user.username
        except User.DoesNotExist:
            pass
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {user.username}!')
            return redirect('index')  # Changed to 'index' for base.html
        else:
            messages.error(request, 'Invalid username/email or password')
            return render(request, 'authentication/login.html')
            
    return render(request, 'authentication/login.html')

@login_required
def index(request):
    return render(request, 'base.html')

def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if User.objects.filter(email=email).exists():
            # Send password reset email logic here
            messages.success(request, 'Password reset link has been sent to your email')
            return redirect('login')
        else:
            messages.error(request, 'No account found with that email')
            
    return render(request, 'authentication/reset-password.html')

def set_new_password_view(request, uidb64, token):
    if request.method == 'POST':
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get