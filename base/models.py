from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FutureOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length = 200)
    leverage = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2)
    take_profit = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
