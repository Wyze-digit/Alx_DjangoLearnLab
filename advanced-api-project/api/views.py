from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListCreateAPIView):
    """
    API view for retrieving a list of all books or creating a new book.
    
    - GET: Returns a list of all Book instances.
    - POST: Creates a new Book instance.
    """
    queryset = Book.objects.all().order_by('-id')  # Order by newest first
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Example of customizing the create behavior
    def perform_create(self, serializer):
        """Automatically set the book's creator to the current user upon creation."""
        serializer.save(creator=self.request.user)

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific book by its ID.
    
    - GET: Retrieve a specific book.
    - PUT: Update all fields of a specific book.
    - PATCH: Partially update fields of a specific book.
    - DELETE: Delete a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Example of customizing the update behavior
    def perform_update(self, serializer):
        """You could add custom logic here, like logging changes."""
        # Example: print(f"Book {serializer.instance.id} was updated by {self.request.user}")
        serializer.save() 
