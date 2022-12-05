from rest_framework import serializers
from core.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    premium_user = serializers.BooleanField()
    price = serializers.BooleanField()


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
    premium_user = serializers.BooleanField()


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
    premium_user = serializers.BooleanField()
