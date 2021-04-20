from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # Your URLs...
    path('create_request', views.create_request, name='create user'),   
    path('get_logs', views.get_logs, name='get logs'),
    path('get_requests', views.get_requests, name='get request'), 
    path('get_issuebook', views.get_issuebook, name='get issuebook'), 
    path('action_request', views.action_request, name='action request'),
    path('return_equipment', views.return_equipment, name='return equipment'),
]
