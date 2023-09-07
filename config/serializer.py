from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'username': None})
        if not attrs['password1'] == attrs['password2']:
            raise serializers.ValidationError({'password': None})
        return attrs

