from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    names = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = 'user_info'
        verbose_name_plural = 'user_info'

    def __str__(self) -> str:
        return self.names