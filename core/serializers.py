from rest_framework import serializers
from user.serializers import RegisterSerializer


class FriendsSerializer(serializers.Serializer):
    main_user = serializers.PrimaryKeyRelatedField(read_only=True)
    friend_user = serializers.PrimaryKeyRelatedField(read_only=True)
    friends = serializers.BooleanField()


class GetFriendsSerializer(serializers.Serializer):
    friend_user = RegisterSerializer()


class PostSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField()
    text = serializers.CharField()

class FeedSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    username=serializers.CharField()
    posts=PostSerializer(many=True)

class FeeedPostSerializer(serializers.Serializer):
    friend_user=FeedSerializer()



class LikeSerializer(serializers.Serializer):
    # likeuser = RegisterSerializer(many=True,read_only=True)
    likepost = serializers.PrimaryKeyRelatedField(read_only=True)
    time = serializers.DateTimeField()
