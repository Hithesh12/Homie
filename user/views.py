from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from core.authentication import MyAuthentication
from core.models import User
from .serializers import RegisterSerializer, UserListSerializer, EditSerializer
import structlog

logger = structlog.get_logger(__name__)
logger.info("an_error_occurred")

#Add new user to the DB
@api_view(http_method_names=['post'])
@permission_classes((AllowAny,))
def registration(request):
    logger.info("Enqueuing successful task")
    if request.method == 'POST':
        data = request.data
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response({'error': 'Please fill all the required field'}, status=HTTP_400_BAD_REQUEST)

#Login and return token to the user
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    logger.info("Enqueuing successful task")
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)

    if user is None:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    register = User.objects.get(email=email)
    serializer = RegisterSerializer(register)
    user_data = {
        'token': token.key,
        'user': serializer.data
    }
    return Response(user_data, status=HTTP_200_OK)

#Display all the user in the DB
@api_view(http_method_names=["get"])
def userlist(request):
    logger.info("Enqueuing successful task")
    if request.method == 'GET':
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

#Fetch a particullar user by id and display,update,delete the data from DB
@api_view(http_method_names=["get", "delete", "put"])
@authentication_classes([MyAuthentication])
def edit(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        raise ValidationError("user doesnot exist")
    logger.info(f'USER-->{request.user.id}')

    if request.method == 'GET':
        serializer = EditSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = request.data
        user.username = data['username']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.phone = data['phone']
        user.modified_by = data['username']
#update the membership from normal user to premium user
        user.premium_user=data['premium_user']
        user.price=data['price']

        premium_user=data['premium_user']
        price=data['price']
        if premium_user is False:
                user.save()
                return Response('sucesfull')

        elif premium_user is True and price is False:
                raise ValidationError('make payment')
                
        elif premium_user is True and price is True:
                user.save()
        return Response('sucesfull')
        
    elif request.method == 'DELETE':
        Token.objects.get(user=user).delete()
        user.delete()
        return Response(f"deleted sucesfully")
