from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('books/', BooksAPIView.as_view(), name='books'),
    path('books/<int:pk>/', BooksDetailAPIView.as_view(), name='book-detail'),
    path('books/delete/<int:pk>/', DeleteBookAPIView.as_view(), name='delete-book'),
]
