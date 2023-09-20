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


class BooksListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.all()
            serializer = self.get_serializer(books, many=True)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            serializer = BookCreateSerializer(request.data)
            name = serializer.data['name']
            description = serializer.data['description']
            author = serializer.data['author']
            pages = serializer.data['pages']
            genre = serializer.data['genre']
            image = request.FILES.get('image')
            Book.objects.create(
                name=name,
                description=description,
                author=author,
                pages=pages,
                genre=genre,
                image=image
            )
            return status201response(serializer.data)
        except:
            return status500response()


class BooksDetailAPIView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Book.objects.filter(pk=pk).exists():
                return status404response(msg='کتاب مورد نظر یافت نشد')
            book_info = Book.objects.get(pk=pk)
            serializer = self.get_serializer(book_info)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Book.objects.filter(pk=pk).exists():
                return status404response(msg='کتاب مورد نظر یافت نشد')
            serializer = BookCreateSerializer(request.data)
            book_info = Book.objects.get(pk=pk)
            name = serializer.data['name']
            description = serializer.data['description']
            author = serializer.data['author']
            pages = serializer.data['pages']
            genre = serializer.data['genre']
            image = request.FILES.get('image')
            book_info.name = name
            book_info.description = description
            book_info.author = author
            book_info.pages = pages
            book_info.genre = genre
            book_info.image = image
            book_info.save()
            return status201response(serializer.data)
        except:
            return status500response()


class DeleteBookAPIView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not Book.objects.filter(pk=pk).exists():
            return status404response(msg='کتاب مورد نظر یافت نشد')
        book_info = Book.objects.get(pk=pk)
        book_info.delete()
        return status204response()


class ReviewsListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            reviews = Review.objects.all()
            serializer = self.get_serializer(reviews, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class ReviewCreatAPIView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = ReviewCreateSerializer(request.data)
            user = request.user
            book = serializer.data['book']
            pages_read = serializer.data['pages_read']
            rating = serializer.data['rating']
            if not Book.objects.filter(pk=book).exists():
                return status404response(msg='کتاب مورد نظر یافت نشد')
            book_info = Book.objects.get(pk=book)
            Review.objects.create(
                name=user,
                book=book_info,
                pages_read=pages_read,
                rating=rating
            )
            return status201response(serializer.data)
        except:
            return status500response()


class ReviewDetailAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Review.objects.filter(pk=pk).exists():
                return status404response(msg='نظر مورد نظر یافت نشد')
            review = Review.objects.get(pk=pk)
            serializer = self.get_serializer(review)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Review.objects.filter(pk=pk).exists():
                return status404response(msg='نظر مورد نظر یافت نشد')
            review = Review.objects.get(pk=pk)
            serializer = ReviewCreateSerializer(request.data)
            book = serializer.data['book']
            pages_read = serializer.data['pages_read']
            rating = serializer.data['rating']
            if not Book.objects.filter(pk=book).exists():
                return status404response(msg='کتاب مورد نظر یافت نشد')
            book_info = Book.objects.get(pk=book)
            review.book = book_info
            review.rating = rating
            review.pages_read = pages_read
            review.save()
            return status201response(serializer.data)
        except:
            return status500response()


class DeleteReviewAPIView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not Review.objects.filter(pk=pk).exists():
            return status404response(msg='نظر مورد نظر یافت نشد')
        review = Review.objects.get(pk=pk)
        review.delete()
        return status204response()


class BookSearchAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '')
        if search_query:
            return Book.objects.filter(models.Q(title__icontains=search_query) |
                                       models.Q(author__icontains=search_query))
        else:
            return Book.objects.all()


class WantsToReadBooksAPIView(generics.ListAPIView):
    serializer_class = WantToReadBooksSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            books = WantToRead.objects.get(user=user)
            serializer = self.get_serializer(books, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class WantsToReadCreateAPIView(generics.CreateAPIView):
    serializer_class = WantToReadBooksCreateSerialzier
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(request.data)
            user = request.user
            books_id = serializer.data['books']
            book_info = []
            for i in range(len(books_id)):
                if not Book.objects.filter(pk=books_id[i]).exists():
                    return status404response(msg='کتاب مورد نظر یافت نشد')
            for i in range(len(books_id)):
                book = Book.objects.get(pk=books_id[i])
                book_info.append(book)
            class_instance = WantToRead.objects.create(
                user=user
            )
            class_instance.books.set(book_info)
            return status200response(serializer.data)
        except:
            return status500response()


class ReadBooksAPIView(generics.ListAPIView):
    serializer_class = WantToReadBooksSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            books = Read.objects.get(user=user)
            serializer = self.get_serializer(books, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class ReadCreateAPIView(generics.CreateAPIView):
    serializer_class = WantToReadBooksCreateSerialzier
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(request.data)
            user = request.user
            books_id = serializer.data['books']
            book_info = []
            for i in range(len(books_id)):
                if not Book.objects.filter(pk=books_id[i]).exists():
                    return status404response(msg='کتاب مورد نظر یافت نشد')
            for i in range(len(books_id)):
                book = Book.objects.get(pk=books_id[i])
                book_info.append(book)
            class_instance = Read.objects.create(
                user=user
            )
            class_instance.books.set(book_info)
            return status200response(serializer.data)
        except:
            return status500response()


class CurrentlyReadingBooksAPIView(generics.ListAPIView):
    serializer_class = WantToReadBooksSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            books = CurrentlyReading.objects.get(user=user)
            serializer = self.get_serializer(books, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class CurrentlyReadingCreateAPIView(generics.CreateAPIView):
    serializer_class = WantToReadBooksCreateSerialzier
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(request.data)
            user = request.user
            books_id = serializer.data['books']
            book_info = []
            for i in range(len(books_id)):
                if not Book.objects.filter(pk=books_id[i]).exists():
                    return status404response(msg='کتاب مورد نظر یافت نشد')
            for i in range(len(books_id)):
                book = Book.objects.get(pk=books_id[i])
                book_info.append(book)
            class_instance = CurrentlyReading.objects.create(
                user=user
            )
            class_instance.books.set(book_info)
            return status200response(serializer.data)
        except:
            return status500response()
