from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes
from .serializers import FriendsSerializer,GetFriendsSerializer,PostSerializer,LikeSerializer,FeedSerializer,FeeedPostSerializer
from .models import Friend_Request, User,Post,Like
from rest_framework.response import Response
from core.authentication import MyAuthentication
from rest_framework.exceptions import ValidationError
from django.db.models import Q 
# Create your views here.

# @login_required
import structlog


logger = structlog.get_logger(__name__)
logger.info("an_error_occurred")

@api_view(http_method_names=['post',"get","delete"])
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

        elif request.method=='DELETE':
            friend=Friend_Request.objects.filter(Q(main_user_id=request.user.id) & Q(friend_user_id=request.data['friend_user_id']) )
            friend.delete()
            return Response('unfriended the user')
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
        if request.method=='DELETE':
            post=Post.objects.filter(user_id=request.user.id)
            post.delete()
    except Exception as e:
            logger.info(event=f'failed', method='post_user', status='failed')
            raise ValidationError({'error': f'(e)',})


@api_view(http_method_names=['get'])
@authentication_classes([MyAuthentication])
def feed(request):
    try:
        if request.method=='GET':
            queryset=Friend_Request.objects.filter(main_user_id=request.user.id)
            serializer=FeeedPostSerializer(queryset,many=True)
            logger.info(event=f'sucessfully-->(e)',
                        method='feed_user', status='sucess')
            return Response(serializer.data)
    except Exception as e:
            logger.info(event=f'failed', method='feed_user', status='failed')
            raise ValidationError({'error': f'(e)',})


# @api_view(http_method_names=['get','post'])
# @authentication_classes([MyAuthentication])
# def likes(request,pk):
#     if request.method=='POST':
#         likeuser=request.user
#         likepost=Post.objects.filter(pk=pk)
#         check=Like.objects.filter(Q(likeuser=likeuser) & Q(likepost=likepost.last()))
#         if check.exists():
#             return Response('already liked')
#         newuser=Like.objects.create(likeuser=likeuser,likepost=likepost.last())
#         newuser.save()
#         seriealizer=LikeSerializer(newuser)
#         return Response(seriealizer.data)

