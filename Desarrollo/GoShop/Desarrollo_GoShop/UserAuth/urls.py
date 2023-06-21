from django.urls import path, include
from . import views_access

urlpatterns = [
    path('login/', views_access.signin, name='signin'),
    path('register/', views_access.signup, name='signup'),
    path('logout/', views_access.signout, name='logout')
]