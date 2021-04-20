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
from .models import RequestModel, IssueBookModel, LogModel
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logs(request):
    user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    user_demanding_requests = UserModel.objects.get(phone_number= user_phone_number) 

    if user_demanding_requests.is_manager:
        logs = LogModel.objects.all()
   
    else:
        logs =  LogModel.objects.filter(requested_by_user=user_demanding_requests)
    
    d= {}
    for log in logs:
        d[log.request_id] =  [log.equipment.equipment_name, log.request_granted]
    
    return JsonResponse(d)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issuebook(request):
    user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    user_demanding_requests = UserModel.objects.get(phone_number= user_phone_number) 

    if user_demanding_requests.is_manager:
        logs = IssueBookModel.objects.all()
   
    else:
        logs = IssueBookModel.objects.filter(requested_by_user=user_demanding_requests)
    
    d= {}
    for log in logs:
        d[log.issue_id] =  [str(log.equipment.equipment_id) + "--> " +log.equipment.equipment_name, log.requested_by_user.first_name + " " + log.requested_by_user.last_name, log.actioned_by.first_name+ " "+ log.actioned_by.last_name]
    
    return JsonResponse(d)


    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def action_request(request):
    user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    actioned_by = UserModel.objects.get(phone_number= user_phone_number) 
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    request_id = body["request_id"]
    is_granted = body["is_granted"]

    if actioned_by.is_manager:
        if is_granted == "True":
            request = RequestModel.objects.get(request_id = request_id)
            equipment = request.equipment
            requested_by_user = request.requested_by_user

            issue_book = IssueBookModel(equipment=equipment,requested_by_user=requested_by_user, actioned_by=actioned_by)
            

            EquipmentModel.objects.filter(equipment_id=equipment.equipment_id).update(is_available=False)

            log = LogModel(request_id=request_id, request_granted=is_granted, equipment=equipment, requested_by_user=request.requested_by_user, actioned_by=actioned_by)
            issue_book.save()
            log.save()
            RequestModel.objects.filter(request_id=request.request_id).delete()
            return HttpResponse("Request Granted Successfully")
        
        else:
            request = RequestModel.objects.get(request_id = request_id)
            equipment = request.equipment
            requested_by_user = request.requested_by_user
            log = LogModel(request_id=request_id, request_granted=False, equipment=equipment, requested_by_user=requested_by_user, actioned_by=actioned_by)
            log.save()

            RequestModel.objects.filter(request_id=request.request_id).delete()
            return HttpResponse("Request Rejected Successfully ")
        
    else:
        return HttpResponse("Please contact manager to take action")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_equipment(request):
    user_phone_number = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    returning_user = UserModel.objects.get(phone_number= user_phone_number) 
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    issue_id = body["issue_id"]
    equipemnt_id = body["equipment_id"]


    issuebook = IssueBookModel.objects.get(issue_id=issue_id)

    if issuebook.requested_by_user == returning_user:
        IssueBookModel.objects.get(issue_id=issue_id).delete()
        EquipmentModel.objects.filter(equipment_id = equipemnt_id).update(is_available=True)
        return HttpResponse("Equipment has been returned successfully")

    
    else:
        return HttpResponse("Invalid request. Please contact manager for further aassistance")