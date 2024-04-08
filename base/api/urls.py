from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_routes, name='api_home'),
    path('create_future_order/',views.create_future_order, name='create_future_order'),
    
]