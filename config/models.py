from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=400)
    author = models.CharField(max_length=255)
    ratings = models.PositiveIntegerField(default=0)
    average = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.00'))
    pages = models.PositiveIntegerField()
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
    name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    pages_read = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f'{self.book.name} ---- {self.rating}'

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        self.book.ratings += 1
        self.book.save()
        self.update_average()

    def delete(self, *args, **kwargs):
        super(Review, self).delete(*args, **kwargs)
        self.book.ratings -= 1
        self.book.save()
        self.update_average()

    def update_average(self):
        reviews = self.book.reviews.all()
        total_ratings = sum(review.rating for review in reviews)
        num_reviews = len(reviews)

        if num_reviews > 0:
            average_rating = total_ratings / num_reviews
        else:
            average_rating = 0

        self.book.average = average_rating
        self.book.save()




