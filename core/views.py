from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes
from .serializers import FriendsSerializer,GetFriendsSerializer,PostSerializer
from .models import Friend_Request, User,Post
from rest_framework.response import Response
from core.authentication import MyAuthentication
from rest_framework.exceptions import ValidationError
# Create your views here.

# @login_required
import structlog


logger = structlog.get_logger(__name__)
logger.info("an_error_occurred")

@api_view(http_method_names=['post',"get"])
@authentication_classes([MyAuthentication])
def friends(request):
    try:
        if request.method=='POST':
            friend_Request = Friend_Request()
            data = request.data
            friend_Request.main_user_id = request.user.id
            friend_Request.friend_user_id = data['friend_user']

            if data['friend_user'] is None:
                return Response('no friend request sent')
            else:
                friend_Request.friends = True
                friend_Request.save()
                return Response(f'friends {friend_Request.friends}')
        
        elif request.method=='GET':
            queryset=Friend_Request.objects.filter(main_user_id=request.user.id)
            serializer=GetFriendsSerializer(queryset,many=True)
            logger.info(event=f'sucessfully-->(e)',
                        method='friends_user', status='sucess')
            return Response(serializer.data)
    except Exception as e:
            logger.info(event=f'failed', method='frieds_user', status='failed')
            raise ValidationError({'error': f'(e)',})

@api_view(http_method_names=['post'])
@authentication_classes([MyAuthentication])
def post(request):
    try:
        post=Post()
        if request.method=='POST':
            post=Post()
            data=request.data
            post.user_id=request.user.id
            post.title=data['title']
            post.text=data['text']
            post.save()
            logger.info(event=f'sucessfully-->(e)',
                        method='post_user', status='sucess')
            return Response('posted')
    except Exception as e:
            logger.info(event=f'failed', method='post_user', status='failed')
            raise ValidationError({'error': f'(e)',})


@api_view(http_method_names=['get'])
@authentication_classes([MyAuthentication])
def feed(request):
    try:
        if request.method=='GET':
            queryset=Post.objects.filter(user_id=request.user.id)
            serializer=PostSerializer(queryset,many=True)
            logger.info(event=f'sucessfully-->(e)',
                        method='feed_user', status='sucess')
            return Response(serializer.data)
    except Exception as e:
            logger.info(event=f'failed', method='feed_user', status='failed')
            raise ValidationError({'error': f'(e)',})