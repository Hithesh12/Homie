from rest_framework import serializers
from core.models import User
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            created_by=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 
        
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

class UserListSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    created = serializers.DateTimeField()
    created_by = serializers.CharField()
    modified = serializers.DateTimeField()
    modified_by = serializers.CharField()

class EditSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    created = serializers.DateTimeField()
    created_by = serializers.CharField()
    modified = serializers.DateTimeField()
    modified_by = serializers.CharField()
