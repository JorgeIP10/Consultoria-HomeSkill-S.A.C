from django.urls import path
from . import views_profile

urlpatterns = [
    path('profile/', views_profile.user_profile, name='profile'),
    path('profile/config', views_profile.user_config, name='config'),
    path('profile/config/confirm/<str:previous_view>/<str:previous_name>/<str:mode>', views_profile.confirm_user_config, name='confirm_user_config'),
    path('profile/history', views_profile.shopping_history, name='history'),
]