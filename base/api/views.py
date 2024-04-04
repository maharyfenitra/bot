from rest_framework.decorators import api_view
from rest_framework.response import Response

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