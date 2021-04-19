from django.shortcuts import render

# Create your views here.
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
from .models import EquipmentModel
from users.models import UserModel
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_equipment(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    equipment_name = body["equipment_name"]
    is_available= bool(body["is_available"])
    
    user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    user_who_added_equipment = UserModel.objects.get(phone_number= user_phone_number)  
    added_by_user = user_who_added_equipment
    
    equipment= EquipmentModel(equipment_name=equipment_name, is_available=is_available,added_by_user = added_by_user)
    equipment.save()
    return HttpResponse("Equipment addition successful")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_equipment(request):
    equipments = EquipmentModel.objects.filter(is_available=True)
    print(equipments)
    d= {}
    for equipment in equipments:
        d[equipment.equipment_id] = equipment.equipment_name
    print(d)
    return  JsonResponse(d)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_equipment(request):
    user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    user = UserModel.objects.get(phone_number= user_phone_number) 

    if user.is_manager:
        equipments = EquipmentModel.objects.all()
        print(equipments)
        d= {}
        for equipment in equipments:
            d[equipment.equipment_id] = equipment.equipment_name
        print(d)
        return  JsonResponse(d)
    else:
        return HttpResponse("Please ask your manager for this list of equipments")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def issued_equipment(request):
    user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    user = UserModel.objects.get(phone_number= user_phone_number) 

    if user.is_manager:
        equipments = EquipmentModel.objects.filter(is_available=False)
        print(equipments)
        d= {}
        for equipment in equipments:
            d[equipment.equipment_id] = equipment.equipment_name
        print(d)
        return  JsonResponse(d)
    else:
        return HttpResponse("Please ask your manager for this list of equipments")