from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import BookReviewForm
from django.views.generic.edit import FormMixin


# Create your views here.
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status='g').count()
    # num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    kontext = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors,
               'num_visits': num_visits
               }

    return render(request, 'index.html', context=kontext)


def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)

    kontext = {
        'authors': paged_authors
    }

    return render(request, 'authors.html', context=kontext)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    template_name = 'book_list.html'


class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    form_class = BookReviewForm

    class Meta:
        ordering = ['title']

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)


def search(request):
    query_text = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query_text) | Q(summary__icontains=query_text)
                                         | Q(isbn__icontains=query_text))
    return render(request, 'search.html', {'books': search_results, 'querytxt': query_text})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance  # konteksto kint i sablona bookinstance_list
    template_name = 'user_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).filter(status__exact='p').order_by('due_back')


@csrf_protect
def register(request):
    if request.method == 'POST':
        # imam laukus is formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password2 == password:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'El. paštas {email} užimtas!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f'Vartotojas {username} sukurtas!')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')
