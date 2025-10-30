# api/urls.py
from django.urls import path
from . import views

# App name for namespacing (useful for reverse URL lookups)
app_name = 'api'

urlpatterns = [
    # Endpoint for listing all books and creating a new one
    path('books/', views.BookListView.as_view(), name='book-list'),
    # Endpoint for retrieving, updating, or deleting a single book by its primary key
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]

