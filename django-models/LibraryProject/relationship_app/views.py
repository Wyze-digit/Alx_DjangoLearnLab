

# Create your views here.
from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all()   # <-- required query
    return render(request, "relationship_app/list_books.html", {"books": books})  # <-- required template


# others
from django.shortcuts import render, get_object_or_404
from .models import Library 

from django.views.generic.detail import DetailView

def library_detail(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    return render(request, 'relationship_app/library_detail.html', {'library': library})

