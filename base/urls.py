from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('trade/',views.trade, name='trade'),
    path('login/',views.login_page, name='login'),
    path('logout/',views.logout_page, name='logout'),
    path('register/',views.register_page, name='register'),
    path('blank/',views.blank_page, name='blank'),
]