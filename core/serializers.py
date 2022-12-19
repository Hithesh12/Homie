from rest_framework import serializers
from user.serializers import RegisterSerializer,UserListSerializer


class FriendsSerializer(serializers.Serializer):
    main_user = serializers.PrimaryKeyRelatedField(read_only=True)
    friend_user = serializers.PrimaryKeyRelatedField(read_only=True)
    friends = serializers.BooleanField()


class GetFriendsSerializer(serializers.Serializer):
    friend_user = RegisterSerializer()

class PostSerializer(serializers.Serializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField()
    text = serializers.CharField()
    total=serializers.SerializerMethodField()

    def get_total(self,instance):
        return instance.like.count()

class ImageSerializer(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.ImageField()

class FeedSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    posts = PostSerializer(many=True)
    image = ImageSerializer(many=True)

class FeedPostSerializer(serializers.Serializer):
    friend_user = FeedSerializer()

class ProfileSerializer(serializers.Serializer):
    profilepic= serializers.ImageField()
    user=serializers.PrimaryKeyRelatedField(read_only=True)




