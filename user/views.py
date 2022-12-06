from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .helper import check,check_premium_update
from core.authentication import MyAuthentication
from core.models import User
from .serializers import RegisterSerializer, UserListSerializer, EditSerializer
import structlog


logger = structlog.get_logger(__name__)
logger.info("an_error_occurred")

# Add new user to the DB
@api_view(http_method_names=['post'])
@permission_classes((AllowAny,))
def registration(request):
    try:
        logger.info("Enqueuing successful task")
        if request.method == 'POST':
            data = request.data
            # Method to validate and save user to the DB
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                user = User()
                user.username = validated_data['username']
                user.phone = validated_data['phone']
                user.email = validated_data['email']
                user.first_name = validated_data['first_name']
                user.last_name = validated_data['last_name']
                user.created_by = validated_data['username']
                user.premium_user = validated_data['premium_user']
                user.price = validated_data['price']
                user.set_password(validated_data['password'])
        # Validation for premium user
                user.check=check(validated_data['price'],validated_data['premium_user'],user,serializer)

        if serializer.is_valid():
            user.save()
            return Response(serializer.data)

        logger.info(event=f'registered sucessfully-->(e)',
                    method='register_user', status='sucess')
        return Response({'error': 'Please fill all the required field'}, status=HTTP_400_BAD_REQUEST)
   
    except Exception as e:
        logger.info(event=f'registration failed',
                    method='register_user', status='failed')
        raise ValidationError({'error': f'(e)'})


# Login and return token to the user
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    try:
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
        logger.info(event=f'logged sucessfully-->(e)',
                    method='login_user', status='sucess')
        return Response(user_data, status=HTTP_200_OK)
    except Exception as e:
        logger.info(event=f'login failed',
                    method='login_user', status='failed')
        raise ValidationError({'error': f'(e)'})


# Display all the user in the DB
@api_view(http_method_names=["get"])
@permission_classes((IsAdminUser,))
def userlist(request):
    logger.info("Enqueuing successful task")
    if request.method == 'GET':
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)


# Fetch a particullar user by id and display,update,delete the data from DB
@api_view(http_method_names=["get", "delete", "put"])
@authentication_classes([MyAuthentication])
def edit(request):
    try:
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
        # update the membership from normal user to premium user
            user.premium_user = data['premium_user']
            user.price = data['price']
            user.check=check_premium_update(data['price'],data['premium_user'],user)
            return Response('sucessfull')
            

        elif request.method == 'DELETE':
            Token.objects.get(user=user).delete()
            user.delete()
            logger.info(event=f'sucessfully-->(e)',
                        method='edit_user', status='sucess')
            return Response(f"deleted sucesfully")
    except Exception as e:
        logger.info(event=f'failed', method='edit_user', status='failed')
        raise ValidationError({'error': f'(e)',})
