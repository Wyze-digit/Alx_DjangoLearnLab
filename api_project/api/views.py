from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """API view to list all books in the database."""
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
