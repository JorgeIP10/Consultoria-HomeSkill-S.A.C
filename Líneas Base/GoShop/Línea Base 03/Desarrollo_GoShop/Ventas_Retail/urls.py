from django.urls import path
from . import views_shop
urlpatterns = [
    path('', views_shop.shop, name='shop'),
    path('kitchen/', views_shop.kitchen, name='kitchen'),
    path('bathroom/', views_shop.bathroom, name='bathroom'),
    path('bedroom/', views_shop.bedroom, name='bedroom'),
    path('decor/', views_shop.decor, name='decor'),
    path('offers/', views_shop.offers, name='offers'),
    path('products/<str:text>', views_shop.get_products, name='get_products'),
    path('<str:view_name>/description/<int:product_id>', views_shop.product_description, name='description'),
]