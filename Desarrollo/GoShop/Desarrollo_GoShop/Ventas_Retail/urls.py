from django.urls import path
from . import views_access,views_profile, views_shop, views_shopping_cart, views_purchase

urlpatterns = [
    path('', views_shop.shop, name='shop'),
    path('login/', views_access.signin, name='signin'),
    path('register/', views_access.signup, name='signup'),
    path('logout/', views_access.signout, name='logout'),
    path('kitchen/', views_shop.kitchen, name='kitchen'),
    path('bathroom/', views_shop.bathroom, name='bathroom'),
    path('bedroom/', views_shop.bedroom, name='bedroom'),
    path('decor/', views_shop.decor, name='decor'),
    path('offers/', views_shop.offers, name='offers'),
    path('products/<str:text>', views_shop.get_products),
    path('<str:view_name>/description/<int:product_id>', views_shop.product_description, name='description'),
    path('profile/', views_profile.user_profile, name='profile'),
    path('profile/config', views_profile.user_config, name='config'),
    path('profile/config/<str:username>', views_profile.change_username),
    path('profile/config/change/password', views_profile.change_password),
    path('profile/payment', views_profile.user_payment, name='payment'),
    path('profile/payment/add_payment_method', views_profile.add_payment_method),
    path('profile/payment/remember_payment_method', views_profile.remember_payment_method),
    path('shopping_cart/', views_shopping_cart.shopping_cart, name='cart'),
    path('shopping_cart/<int:product_id>', views_shopping_cart.get_product_quantity_cart),
    path('shopping_cart/buy', views_purchase.buy_product, name='buy'),
    path('shopping_cart/buy/<str:number>/<str:month>/<str:year>/<str:cvv>/<str:remember>', views_purchase.verify_card),
    path('products/add_product/<int:product_id>', views_shopping_cart.add_product),
    path('products/remove_product_unit/<int:product_id>', views_shopping_cart.remove_product_unit),
    path('products/remove_product/<int:product_id>', views_shopping_cart.remove_product)
]