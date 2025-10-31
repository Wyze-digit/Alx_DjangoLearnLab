from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# Create your views here.
# api/views.py
from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend 


class BookListView(generics.ListAPIView):
    """
    API view for retrieving a list of all books.
    - GET: Returns a list of all Book instances.
    """
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    # DjangoFilterBackend configuration
    filterset_class = BookFilter 

    # Configure filter backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 

    # SearchFilter configuration
    search_fields = ['title', 'author', 'description'] 

    # OrderingFilter configuration
    ordering_fields = ['title', 'author', 'publication_year', 'created_at', 'updated_at']
    ordering = ['-created_at']  # Default ordering 


class BookDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a single book by ID.
    - GET: Retrieve a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    

class BookCreateView(generics.CreateAPIView):
    """
    API view for creating a new book.
    - POST: Creates a new Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be authenticated to create

    def perform_create(self, serializer):
        """Automatically set the book's creator to the current user upon creation."""
        serializer.save(creator=self.request.user)

class BookUpdateView(generics.UpdateAPIView):
    """
    API view for modifying an existing book.
    - PUT: Update all fields of a specific book.
    - PATCH: Partially update fields of a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be authenticated to update

    def perform_update(self, serializer):
        """You could add custom logic here, like logging changes."""
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    API view for removing a book.
    - DELETE: Delete a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be authenticated to delete

    def perform_destroy(self, instance):
        """You could add custom logic here before deletion."""
        # Example: logging, cleanup, etc.
        super().perform_destroy(instance)