from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def trade(request):
    if request.method == 'POST':
        return redirect('trade')
    return render(request, 'base/trade.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user =authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password incorrect')
        
    return render(request, 'base/login.html')

def logout_page(request):
    logout(request)
    return redirect("home")

def register_page(request):
    form = UserCreationForm()
    context = {"form": form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occur during registration')
    return render(request, 'base/register.html', context)

def order(request):
    return render(request, 'base/order.html')

def blank_page (request):
    return render(request, 'blank.html')
