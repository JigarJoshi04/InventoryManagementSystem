from django.shortcuts import render,HttpResponse
import requests
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
from equipments.models import EquipmentModel
from users.models import UserModel
from .models import RequestModel
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_request(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    equipment_id = body["equipment_id"]

    if EquipmentModel.objects.get(equipment_id=equipment_id).is_available:
        equipment = EquipmentModel.objects.get(equipment_id=equipment_id)
        user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
        user_who_requested = UserModel.objects.get(phone_number= user_phone_number)  
        requested_by_user = user_who_requested

        request=  RequestModel(equipment=equipment, requested_by_user= requested_by_user)
        request.save()

        return HttpResponse("Request Successfully Made")
    
    else:
        return HttpResponse("Request Failed as the item is not available")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_requests(request):
    user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    user_demanding_requests = UserModel.objects.get(phone_number= user_phone_number) 

    if user_demanding_requests.is_manager:
        requests = RequestModel.objects.all()
   
    else:
        requests =  RequestModel.objects.filter(requested_by_user=user_demanding_requests)
    
    d= {}
    for request in requests:
        d[request.request_id] =  [request.equipment.equipment_name, request.requested_by_user.first_name + " " +request.requested_by_user.last_name]
    
    return JsonResponse(d)
    
