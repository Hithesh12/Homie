from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import FriendsSerializer, GetFriendsSerializer,ProfileSerializer, PostSerializer, FeedPostSerializer, FeedSerializer, ImageSerializer
from .models import Friend_Request, User, Post, UploadImageTest,ProfileUser
from rest_framework.response import Response
from core.authentication import MyAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.db.models import Q
# Create your views here.

# @login_required
import structlog


logger = structlog.get_logger(__name__)
logger.info("an_error_occurred")


@api_view(http_method_names=['post', "get", "delete"])
@authentication_classes([MyAuthentication])
def friends(request):
    try:
        if request.method == 'POST':
            friend_Request = Friend_Request()
            data = request.data
            friend_Request.main_user_id = request.user.id
            friend_Request.friend_user_id = data['friend_user']

            if data['friend_user'] is None:
                return Response('no friend request sent')
            elif Friend_Request.objects.filter(main_user_id=request.user.id).filter(friend_user_id= data['friend_user']).exists():
                return Response('already friends')

            friend_Request.friends = True
            friend_Request.save()
            return Response(f'friends {friend_Request.friends}')

        elif request.method == 'GET':
            queryset = Friend_Request.objects.filter(
                main_user_id=request.user.id)
            serializer = GetFriendsSerializer(queryset, many=True)
            logger.info(event=f'sucessfully-->(e)',
                        method='friends_user', status='sucess')
            return Response(serializer.data)

        elif request.method == 'DELETE':
            friend = Friend_Request.objects.filter(Q(main_user_id=request.user.id) & Q(
                friend_user_id=request.data['friend_user_id']))
            friend.delete()
            return Response('unfriended the user')
    except Exception as e:
        logger.info(event=f'failed', method='frieds_user', status='failed')
        raise ValidationError({'error': f'(e)', })


@api_view(http_method_names=['post'])
@authentication_classes([MyAuthentication])
def post(request):
    try:
        post = Post()
        if request.method == 'POST':
            post = Post()
            data = request.data
            post.user_id = request.user.id
            post.title = data['title']
            post.text = data['text']
            post.save()
            logger.info(event=f'sucessfully-->(e)',
                        method='post_user', status='sucess')
            return Response('posted')
        if request.method == 'DELETE':
            post = Post.objects.filter(user_id=request.user.id)
            post.delete()
    except Exception as e:
        logger.info(event=f'failed', method='post_user', status='failed')
        raise ValidationError({'error': f'(e)', })


@api_view(http_method_names=['get'])
@authentication_classes([MyAuthentication])
def feed(request):
    try:
        if request.method == 'GET':
            queryset = Friend_Request.objects.filter(
                main_user_id=request.user.id)
            serializer = FeedPostSerializer(queryset, many=True)
            logger.info(event=f'sucessfully-->(e)',
                        method='feed_user', status='sucess')
            return Response(serializer.data)
    except Exception as e:
        logger.info(event=f'failed', method='feed_user', status='failed')
        raise ValidationError({'error': f'(e)', })


@api_view(http_method_names=['delete', 'post'])
@authentication_classes([MyAuthentication])
def likes(request, pk):
    try:
        if request.method == 'POST':
            user = request.user.id
            post = Post.objects.get(pk=pk)
            post.like.add(User.objects.get(pk=user).id)
            return Response('liked')
        if request.method == 'DELETE':
            post.like.remove(User.objects.get(pk=user).id)
            logger.info(event=f'sucessfully-->(e)',
                        method='likes_user', status='sucess')
            return Response("unliked")
    except Exception as e:
        logger.info(event=f'failed', method='likes_user', status='failed')
        raise ValidationError({'error': f'(e)', })


@api_view(http_method_names=['post'])
@authentication_classes([MyAuthentication])
def Image(request):
    try:
        if request.method=='POST':

            # queryset = UploadImageTest.objects.all()
            serializer_class = ImageSerializer(data=request.data)
            if serializer_class.is_valid():
                upload=UploadImageTest()
                upload.user=request.user
                upload.name=request.data['name']
                upload.image=request.data['image']
                upload.save()
                return Response('uploaded')
    except Exception as e:
        logger.info(event=f'failed', method='image_user', status='failed')
        raise ValidationError({'error': f'(e)', })

@api_view(http_method_names=['DELETE'])
@authentication_classes([MyAuthentication])
def ImageDel(request,pk):
    if request.method=='DELETE':
        upload=UploadImageTest.objects.get(pk=pk)
        upload.image.delete()
        upload.delete()
        return Response('deleted sucesfully')

@api_view(http_method_names=['delete', 'post'])
@authentication_classes([MyAuthentication])
def likeimage(request, pk):
    try:
        upload=UploadImageTest.objects.get(pk=pk)
        if request.method == 'POST':
            user = request.user.id
            upload.likes.add(request.user.id )
            return Response('liked')
        if request.method == 'DELETE':
            upload.likes.remove(request.user.id)
            logger.info(event=f'sucessfully-->(e)',
                        method='likes_user', status='sucess')
            return Response("unliked")
    except Exception as e:
        logger.info(event=f'failed', method='likeimage_user', status='failed')
        raise ValidationError({'error': f'(e)', })


@api_view(http_method_names=['post'])
@authentication_classes([MyAuthentication])
def Profile(request):
    # try:
        if request.method=='POST':

            serializer_class = ProfileSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                upload=ProfileUser()
                upload.user_id=request.user.id
                upload.profilepic=request.data['profilepic']
                upload.save()
                return Response('uploaded')
    # except Exception as e:
    #     logger.info(event=f'failed', method='profile_user', status='failed')
    #     return Response({'error': f'(e)', })