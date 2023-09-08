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


class ReviewSerializer(serializers.ModelSerializer):

    def get_book(self, obj):
        return obj.book.name

    book = serializers.SerializerMethodField('get_book', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewCreateSerializer(serializers.Serializer):
    book = serializers.IntegerField()
    pages_read = serializers.IntegerField()
    rating = serializers.IntegerField()


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class BookCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    author = serializers.CharField()
    pages = serializers.IntegerField()
    image = serializers.ImageField()

