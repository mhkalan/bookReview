from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]
