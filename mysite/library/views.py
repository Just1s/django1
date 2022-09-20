from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, BookInstance, Author, Genre


# Create your views here.
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status='g').count()
    # num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.count()
    kontext = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors}

    return render(request, 'index.html', context=kontext)


def authors(request):
    autoriai = Author.objects.all()
    kontext = {
        'authors': autoriai
    }

    return render(request, 'authors.html', context=kontext)
