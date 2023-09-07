from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .serializer import *
from .models import *
from .utils import *

User = get_user_model()

# Create your views here


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return status404response(msg='چنین کاربری وجود ندارد')
            if not user.is_superuser and not user.is_staff:
                return status401response()
            access = AccessToken.for_user(user)
            data = {
                'access': str(access),
            }
            return status200response(data)
        except:
            return status500response()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                errors = serializerError(serializer.errors)
                for e in errors:
                    if e == 'username':
                        return status400response(msg='نام کاربری تکراری است')
                    elif e == 'password':
                        return status400response(msg='پسوردهای وارد شده مشابه نیستند')
                    else:
                        return status500response()
            username = serializer.validated_data.get('username')
            password1 = serializer.validated_data.get('password1')
            User.objects.create(username=username, password=make_password(password1),
                                is_active=True, is_staff=True, is_superuser=False)
            return status200response(serializer.data)
        except:
            return status500response()

