from django.contrib import admin
from .models import ProductCategory, Product, UserInfo, PaymentCard

class ProductCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )

class UserInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )

class PaymentCardAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(PaymentCard, PaymentCardAdmin)