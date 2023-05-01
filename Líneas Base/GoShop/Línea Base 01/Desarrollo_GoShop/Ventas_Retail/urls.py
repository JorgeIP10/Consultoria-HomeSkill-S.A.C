from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('login/', views.signin, name='signin'),
    path('register/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('kitchen/', views.kitchen, name='kitchen'),
    path('bathroom/', views.bathroom, name='bathroom'),
    path('bedroom/', views.bedroom, name='bedroom'),
    path('decor/', views.decor, name='decor'),
    path('offers/', views.offers, name='offers'),
    path('products/<str:text>', views.get_products, name='products'),
    path('<str:view_name>/description/<int:product_id>', views.product_description, name='description'),
]