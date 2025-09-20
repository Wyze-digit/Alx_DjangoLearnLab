

# Create your views here.
from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all()   # <-- required query
    return render(request, "relationship_app/list_books.html", {"books": books})  # <-- required template
