from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# registruoti, kad prieiti admin svetaineje
# Register your models here.

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(BookInstance)
