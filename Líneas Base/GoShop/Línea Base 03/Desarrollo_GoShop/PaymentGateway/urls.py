from django.urls import path, include
from . import views_purchase

urlpatterns = [
    path('shopping_cart/buy', views_purchase.buy_product, name='buy'),
    path('shopping_cart/buy/confirm/<str:previous_view>/<str:previous_name>/<str:mode>', views_purchase.confirm_purchase, name='confirm_purchase'),
    path('shopping_cart/buy/<str:names>/<str:surnames>/<str:dni>/<str:address>', views_purchase.save_user_info),
    path('paypal/', include('paypal.standard.ipn.urls')),
]