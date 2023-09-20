from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('books/', BooksListCreateAPIView.as_view(), name='books'),
    path('books/<int:pk>/', BooksDetailAPIView.as_view(), name='book-detail'),
    path('books/delete/<int:pk>/', DeleteBookAPIView.as_view(), name='delete-book'),
    path('books/search/<str:search>/', BookSearchAPIView.as_view(), name='book-search'),
    path('books/wantsToRead/', WantsToReadBooksAPIView.as_view(), name='wants-to-read'),
    path('books/wantsToRead/create/', WantsToReadCreateAPIView.as_view(), name='wants-to-read-create'),
    path('books/Read/', ReadBooksAPIView.as_view(), name='read'),
    path('books/Read/create/', ReadCreateAPIView.as_view(), name='read-create'),
    path('books/CurrentlyReading/', CurrentlyReadingBooksAPIView.as_view(), name='currently-reading'),
    path('books/CurrentlyReading/create/', CurrentlyReadingCreateAPIView.as_view(), name='currently-reading-create'),
    path('reviews/', ReviewsListAPIView.as_view(), name='reviews'),
    path('reviews/create/', ReviewCreatAPIView.as_view(), name='reviews-create'),
    path('review/<int:pk>', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('reviews/delete/<int:pk>/', DeleteReviewAPIView.as_view(), name='delete-review'),
]
