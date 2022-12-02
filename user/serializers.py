from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    password=serializers.CharField()
    email = serializers.EmailField(unique=True)
    created=serializers.DateTimeField(auto_now=True)
    created_by=serializers.CharField(max_length=255)
    modified=serializers.DateTimeField(auto_now=True)
    modified_by=serializers.CharField(max_length=255)

