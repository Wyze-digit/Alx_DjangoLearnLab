from django.urls import path
from . import views

# App name for namespacing (useful for reverse URL lookups)
app_name = 'api'

urlpatterns = [
    # Endpoint for listing all Books
    path('books/', views.BookListView.as_view(), name='book-list'), 
    # Endpoint for retrieving a single book by ID 
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'), 
    # Endpoint for creating a new book
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    # Endpoint for updating an existing book
    path('books/update/', views.BookUpdateView.as_view(), name='book-update'),
    # Endpoint for deleting a book
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete'), 
    ]

