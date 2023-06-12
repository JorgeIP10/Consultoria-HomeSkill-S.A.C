from django.contrib import admin
from .models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )

admin.site.register(UserInfo, UserInfoAdmin)