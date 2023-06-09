from django.contrib import admin
from .models import ProductCategory, Product, UserProfile, PaymentCard

class ProductCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )

class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )

class PaymentCardAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )

# Register your models here.
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PaymentCard, PaymentCardAdmin)