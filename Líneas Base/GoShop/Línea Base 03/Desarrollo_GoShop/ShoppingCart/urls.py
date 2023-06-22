from django.urls import path
from . import views_shopping_cart

urlpatterns = [
    path('shopping_cart/', views_shopping_cart.shopping_cart, name='cart'),
    path('shopping_cart/<int:product_id>', views_shopping_cart.get_product_quantity_cart, name='get_product_quantity_cart'),
    path('products/add_product/<int:product_id>', views_shopping_cart.add_product, name='add_product'),
    path('products/remove_product_unit/<int:product_id>', views_shopping_cart.remove_product_unit, name='remove_product_unit'),
    path('products/remove_product/<int:product_id>', views_shopping_cart.remove_product, name='remove_product')
]