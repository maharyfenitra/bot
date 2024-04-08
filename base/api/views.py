from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from base.models import FutureOrder
from binance.client import Client
import os 
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ['BINANCE_API_KEY_TEST']
api_secret = os.environ['BINANCE_API_SECRET_TEST']
client = Client(api_key,api_secret, testnet=True)

@api_view(['GET', 'PUT', 'POST'])
def get_routes(request):
    if request.user.is_authenticated:
        routes = [
            'GET /api/rooms',
            'GET /api/rooms/:id'
        ]
        
        return Response(routes)
    else:
        return Response({})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_future_order(request):
    print("Handling post query")
    print(request.POST)
    if request.method == 'POST':
        symbol = request.data['symbol']  # Extract symbol from request data
        leverage = request.data['leverage']
        quantity = request.data['quantity']
        stop_loss = request.data['stop_loss']
        take_profit = request.data['take_profit']

        if not symbol or not leverage or not quantity:
            return Response({'error': 'Please provide all required parameters leverage symbol quantity'}, status=400)

        # Retrieve current user session
        user = request.user

        try:
            order_type = 'MARKET'
            # Execute the order
            order = client.futures_create_order(
                symbol=symbol,
                side='BUY',
                type=order_type,
                quantity=quantity
            )
            # Save order with the current user and symbol
            FutureOrder.objects.create(
                user=user,
                symbol=symbol,
                leverage=leverage,
                quantity=quantity,
                stop_loss=1,
                take_profit=1,
                order_id=order['orderId']
            )

            return Response({'success': 'Future order created successfully'}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
