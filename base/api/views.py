from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'PUT', 'POST'])
def get_routes(request):
    routes = [
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    
    return Response(routes)