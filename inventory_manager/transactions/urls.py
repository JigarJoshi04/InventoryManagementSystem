from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # Your URLs...
    path('create_request', views.create_request, name='create user'),   
    path('get_requests', views.get_requests, name='get request'), 
]
