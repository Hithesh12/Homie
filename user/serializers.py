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
    
#Method to validate and save user to the DB
    def create(self, validated_data):
        user = User()
        user.username=validated_data['username']
        user.phone=validated_data['phone']
        user.email=validated_data['email']
        user.first_name=validated_data['first_name']
        user.last_name=validated_data['last_name']
        user.created_by=validated_data['username']
        user.premium_user=validated_data['premium_user']
        user.price=validated_data['price']
        user.set_password(validated_data['password'])
#Validation for premium user
        premium_user=validated_data['premium_user']
        price=validated_data['price']
        print(validated_data['phone'])
        if premium_user is False:
                user.save()
                return user
        elif premium_user is True and price is False:
                raise ValidationError('make payment')
        elif premium_user is True and price is True:
                user.save()
        return user

       
       
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
