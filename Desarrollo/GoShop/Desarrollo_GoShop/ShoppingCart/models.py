from django.db import models
from django.contrib.auth.models import User

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.JSONField(default=list)

    class Meta:
        db_table = 'shopping_cart'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return f"Cart for {self.user.username}"