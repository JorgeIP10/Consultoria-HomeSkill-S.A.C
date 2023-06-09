from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=20)
    image = models.ImageField(upload_to='shop')
    on_sale = models.BooleanField(default=False, blank=True)
    sale_price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self) -> str:
        return self.name
    
class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.JSONField(default=list)

    class Meta:
        db_table = 'shopping_cart'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'user_profile'
        verbose_name_plural = 'user_profiles'

    def __str__(self) -> str:
        return self.username
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user_id=instance.id, username=instance.username, email=instance.email)
    else:
        UserProfile.objects.filter(user_id=instance.id).update(username=instance.username, email=instance.email)

class PaymentCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=16)
    expiration_month = models.CharField(max_length=2)
    expiration_year = models.CharField(max_length=4)
    expiration_date = models.CharField(max_length=8)
    cvv = models.CharField(max_length=4)
    remembered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_card'
        verbose_name = 'payment_card'
        verbose_name_plural = 'payment_cards'

    def __str__(self) -> str:
        return f'Card of {self.owner.username}'
    
@receiver(post_save, sender=PaymentCard)
def set_expiration_date(sender, instance, created, **kwargs):
    if created:
        instance.expiration_date = f'{instance.expiration_month}-{instance.expiration_year}'
        instance.save()