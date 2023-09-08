from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Book)
admin.site.register(Read)
admin.site.register(CurrentlyReading)
admin.site.register(WantToRead)
admin.site.register(Review)
