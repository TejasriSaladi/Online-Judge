from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.conf import settings
import random
import string



def register_user(request):
    """Handle user registration with OTP verification."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User with this username already exists.')
            return redirect('/auth/login/')
        
       
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.date_joined = timezone.now()
        user.save()
        
        messages.success(request, 'User created successfully. Please check your email for OTP.')
        return redirect('/auth/register/')
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
def login_user(request):
    """Handle user login."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User with this username does not exist.')
            return redirect('/auth/login/')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid password.')
            return redirect('/auth/login/')
        
        login(request, user)
        messages.success(request, 'Login successful.')
        return redirect('/problems/list/')
    
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def logout_user(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('/auth/login/')
