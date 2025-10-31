# api/tests/test_views.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Book
from django.urls import reverse
import json

class BaseAPITestCase(TestCase):
    """
    Base test case with common setup for all API tests
    """
    
    def setUp(self):
        """Set up test data and client"""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            author='William S. Vincent',
            publication_year=2022,
            description='A comprehensive guide to Django'
        )
        self.book2 = Book.objects.create(
            title='Django for APIs',
            author='William S. Vincent',
            publication_year=2021,
            description='Building web APIs with Django'
        )
        self.book3 = Book.objects.create(
            title='Python Crash Course',
            author='Eric Matthes',
            publication_year=2019,
            description='Learn Python programming'
        )
        
        # Initialize API client
        self.client = APIClient()
        
    def authenticate_user(self, user=None):
        """Helper method to authenticate a user"""
        if user is None:
            user = self.user
        self.client.force_authenticate(user=user)
    
    def tearDown(self):
        """Clean up after tests"""
        self.client.logout() 

# THIS PORTION SOLVES CRUD OPERATIONS TEST
# api/tests/test_views.py (continued)

class BookCRUDTests(BaseAPITestCase):
    """
    Test CRUD operations for Book API endpoints
    """
    
    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can list books"""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], self.book1.title)
    
    def test_retrieve_single_book(self):
        """Test retrieving a single book by ID"""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['author'], self.book1.author)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        data = {
            'title': 'New Django Book',
            'author': 'Test Author',
            'publication_year': 2023,
            'description': 'A new book about Django'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Django Book')
        self.assertEqual(Book.objects.count(), 4)  # 3 initial + 1 new
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        url = reverse('api:book-create')
        data = {
            'title': 'Unauthorized Book',
            'author': 'Unauthorized Author',
            'publication_year': 2023
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)  # No new books created
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication"""
        self.authenticate_user()
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Django Book',
            'author': 'Updated Author',
            'publication_year': 2023
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Django Book')
        self.assertEqual(self.book1.author, 'Updated Author')
    
    def test_partial_update_book(self):
        """Test partial update of a book"""
        self.authenticate_user()
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Partially Updated Title'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        # Other fields should remain unchanged
        self.assertEqual(self.book1.author, 'William S. Vincent')
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication"""
        self.authenticate_user()
        
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)  # One book deleted
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)  # No books deleted 

# STEP 4: THIS PORTION SOLVES QUERY FEATURES TESTS
# api/tests/test_views.py (continued)

class BookQueryTests(BaseAPITestCase):
    """
    Test filtering, searching, and ordering functionalities
    """
    
    def test_filter_by_author(self):
        """Test filtering books by author"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': 'William S. Vincent'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 books by William
        for book in response.data:
            self.assertEqual(book['author'], 'William S. Vincent')
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 2021})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for APIs')
    
    def test_filter_by_publication_year_range(self):
        """Test filtering books by publication year range"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year__gt': 2020})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Books from 2021 and 2022
    
    def test_search_functionality(self):
        """Test text search across title and author fields"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Django'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Django books
        for book in response.data:
            self.assertIn('Django', book['title'])
    
    def test_search_by_author_name(self):
        """Test searching by author name"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Eric'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Eric Matthes')
    
    def test_ordering_by_title_ascending(self):
        """Test ordering books by title ascending"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_publication_year_descending(self):
        """Test ordering books by publication year descending"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_combined_query_parameters(self):
        """Test combining multiple query parameters"""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'author': 'William S. Vincent',
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Should be ordered by publication year descending
        self.assertEqual(response.data[0]['publication_year'], 2022)
        self.assertEqual(response.data[1]['publication_year'], 2021) 

# This portion... STEP 5: Solves Authentication and Error handling Test
# api/tests/test_views.py (continued)

class AuthenticationAndErrorTests(BaseAPITestCase):
    """
    Test authentication, permissions, and error handling
    """
    
    def test_unauthenticated_access_to_protected_endpoints(self):
        """Test that unauthenticated users get proper error responses"""
        endpoints = [
            reverse('api:book-create'),
            reverse('api:book-update', kwargs={'pk': self.book1.id}),
            reverse('api:book-delete', kwargs={'pk': self.book1.id}),
        ]
        
        for url in endpoints:
            response = self.client.post(url, {})  # Try to access with empty data
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist"""
        url = reverse('api:book-detail', kwargs={'pk': 9999})  # Non-existent ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_book(self):
        """Test updating a book that doesn't exist"""
        self.authenticate_user()
        
        url = reverse('api:book-update', kwargs={'pk': 9999})
        data = {'title': 'Nonexistent Book'}
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_invalid_data(self):
        """Test creating a book with invalid data"""
        self.authenticate_user()
        
        url = reverse('api:book-create')
        invalid_data = {
            'title': '',  # Empty title - should be invalid
            'author': 'Test Author',
            'publication_year': 'invalid_year'  # Should be integer
        }
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Should have validation errors for title and publication_year
        self.assertIn('title', response.data)
        self.assertIn('publication_year', response.data)
    
    def test_invalid_query_parameters(self):
        """Test API behavior with invalid query parameters"""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'invalid_param': 'value',
            'ordering': 'invalid_field'  # Non-existent field
        })
        
        # Should still return 200 but might ignore invalid parameters
        self.assertEqual(response.status_code, status.HTTP_200_OK) 


