from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import os 
from binance.client import Client
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ['BINANCE_API_KEY_TEST']
api_secret = os.environ['BINANCE_API_SECRET_TEST']
client = Client(api_key,api_secret, testnet=True)


# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def trade(request):
    symbol = 'BTCUSDT'
    if request.method == 'POST':
        
        ticker = client.get_symbol_ticker(symbol=symbol)
        current_price = float(ticker['price'])
        # Define your order parameters
        side = 'BUY'  # Or 'SELL' if you want to take a short position

        # Define the quantity of the contract you want to trade
        quantity = 0.5  # Adjust this based on your desired position size

        # Define the type of order (LIMIT, MARKET, etc.)
        order_type = 'MARKET'  # Or 'LIMIT' if you want to specify a price
        
        # Execute the order
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )
        
        return redirect('trade')
    orders = client.futures_get_all_orders(symbol=symbol)
    
    order = client.futures_get_order(symbol=symbol, orderId=3751436361)
     
    context = { "orders": orders }
    return render(request, 'base/trade.html', context)
def cancel_order(request, pk):
    
    symbol = 'BTCUSDT'
    
    order = client.futures_get_order(symbol=symbol, orderId=pk)

    print(order)
    
    # Determine the opposite side to close the position
    close_side = 'SELL' 
    
    if order['side'] == 'SELL':
        close_side = 'BUY' 
    
    print(close_side)
    
    close_order = client.futures_create_order(
        symbol=symbol,
        side=close_side,
        type='MARKET',
        quantity=float(order['executedQty'])
    )
    
    print(close_order)
    return redirect('trade')

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
