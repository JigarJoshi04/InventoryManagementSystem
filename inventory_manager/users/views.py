from django.shortcuts import render, HttpResponse
from users.models import UserModel
from .serializers import convert_bytes_array_to_json
import requests
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json

# Create your views here.


@csrf_exempt
def create_user(request):

    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        print(body_unicode)
        body = json.loads(body_unicode)
        first_name = body["first_name"]
        last_name = body["last_name"]
        email = body["email"]
        phone_number = body["phone_number"]
        if body["is_manager"] == "False":
            is_manager= False
        else:
            is_manager = True
        str_password = body["password"]
        password = make_password(str_password)
        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_manager=is_manager,
            email=email,
            password=password,
        )
        user.save()

        # users = UserModel.objects.get(phone_number =phone_number)
        # url = 'http://localhost:8000/api/token/'
        # data = {"username":phone_number,"password":str_password}
        # response = requests.post(url, data = data)
        # response_json = convert_bytes_array_to_json(response.content)
        # response_data = {"token" : response_json["token"]}
        response_data = {"status": "User Created"}
        return JsonResponse(response_data)

    else:
        response_data = {"status": "Get request not allowed."}
        return JsonResponse(response_data)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        phone_number = body["phone_number"]
        password = body["password"]

        users = UserModel.objects.get(phone_number=phone_number)

        if users.check_password(password):

            url = "http://localhost:8000/api/token/"
            data = {"username": phone_number, "password": password}
            response = requests.post(url, data=data)
            print(response)
            response_json = convert_bytes_array_to_json(response.content)
            response_data = {"token": response_json["token"]}

            return JsonResponse(response_json)

        else:
            return HttpResponse("Incorrect Credentials. Do check credentials and try again")

    else:
        return HttpResponse("Get request not allowd. Please do post request")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test_api(request):
    print(str(request.headers["Authorization"])[6:])
    user = Token.objects.get(key=str(request.headers["Authorization"])[6:]).user
    print(user)
    return HttpResponse("Test Successful")