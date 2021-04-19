from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # Your URLs...
    path('create_equipment', views.create_equipment, name='create user'),    
]
