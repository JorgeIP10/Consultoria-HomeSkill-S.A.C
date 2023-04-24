from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('login/', views.signin, name='signin'),
    path('register/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
]