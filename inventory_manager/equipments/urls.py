from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # Your URLs...
    path('create_equipment', views.create_equipment, name='create user'),   
    path('available_equipment', views.available_equipment, name='create user'),   
    path('issued_equipment', views.issued_equipment, name='create user'), 
    path('all_equipment', views.all_equipment, name='create user'),  
]
