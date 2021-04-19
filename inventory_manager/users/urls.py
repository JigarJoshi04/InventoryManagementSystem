from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    # Your URLs...
    path('create_user', views.create_user, name='create user'),
    path('login_user', views.login_user, name='login user'),
    path('test_api', views.test_api, name='test api'),
    
]
