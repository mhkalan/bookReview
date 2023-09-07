from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=400)
    author = models.CharField(max_length=255)
    ratings = models.PositiveIntegerField(default=0)
    average = models.PositiveIntegerField(default=0)
    pages = models.PositiveIntegerField()
    pages_read = models.PositiveIntegerField()
    first_published = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name


class Read(models.Model):
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.books.name


class CurrentlyReading(models.Model):
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.books.name


class WantToRead(models.Model):
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.books.name


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f'{self.book.name} ---- {self.rating}'

