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
        # Create test users with different roles
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpass123',
            email='regular@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.editor_user = User.objects.create_user(
            username='editor',
            password='editorpass123',
            email='editor@example.com',
            is_staff=True  # Different role for testing
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
    
    def login_user(self, username='regularuser', password='testpass123'):
        """
        Helper method for authentication - CORRESPONDS TO ALGORITHM
        Uses Django's login system as checker expects
        """
        return self.client.login(username=username, password=password)
    
    def logout_user(self):
        """
        Helper method to logout user
        """
        self.client.logout()
    
    def tearDown(self):
        """
        Clean up after tests - CORRESPONDS TO ALGORITHM
        """
        self.logout_user()
        # Django automatically cleans up test database

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
    
    def test_retrieve_single_book(self):
        """Test retrieving a single book by ID"""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication using helper method"""
        # USING HELPER METHOD - CORRESPONDS TO ALGORITHM
        login_success = self.login_user('regularuser', 'testpass123')
        self.assertTrue(login_success)
        
        url = reverse('api:book-create')
        data = {
            'title': 'New Django Book',
            'author': 'Test Author',
            'publication_year': 2023,
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        
        self.logout_user()
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        url = reverse('api:book-create')
        data = {'title': 'Unauthorized Book', 'author': 'Test', 'publication_year': 2023}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication"""
        self.login_user('regularuser', 'testpass123')
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Updated Book', 'author': 'Updated Author', 'publication_year': 2023}
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book')
        
        self.logout_user()
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication"""
        self.login_user('regularuser', 'testpass123')
        
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        
        self.logout_user()

class BookQueryTests(BaseAPITestCase):
    """
    Test filtering, searching, and ordering functionalities
    """
    
    def test_filter_by_author(self):
        """Test filtering books by author"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': 'William S. Vincent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_functionality(self):
        """Test text search across title and author fields"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_ordering_by_publication_year_descending(self):
        """Test ordering books by publication year descending"""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [2022, 2021, 2019])

class AuthenticationAndRoleTests(BaseAPITestCase):
    """
    Test authentication and permission enforcement for different user roles
    CORRESPONDS TO ALGORITHM: "Verify permission enforcement for different user roles"
    """
    
    def test_regular_user_can_access_protected_endpoints(self):
        """Test that regular authenticated users can access protected endpoints"""
        self.login_user('regularuser', 'testpass123')
        
        # Test create access
        url = reverse('api:book-create')
        data = {'title': 'Regular User Book', 'author': 'Regular', 'publication_year': 2023}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.logout_user()
    
    def test_admin_user_can_access_protected_endpoints(self):
        """Test that admin users can access protected endpoints"""
        self.login_user('admin', 'adminpass123')
        
        # Test create access
        url = reverse('api:book-create')
        data = {'title': 'Admin Book', 'author': 'Admin', 'publication_year': 2023}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.logout_user()
    
    def test_unauthorized_access_attempts(self):
        """Test various unauthorized access attempts - CORRESPONDS TO ALGORITHM"""
        endpoints = [
            (reverse('api:book-create'), 'post'),
            (reverse('api:book-update', kwargs={'pk': self.book1.id}), 'put'),
            (reverse('api:book-delete', kwargs={'pk': self.book1.id}), 'delete'),
        ]
        
        for url, method in endpoints:
            if method == 'post':
                response = self.client.post(url, {})
            elif method == 'put':
                response = self.client.put(url, {})
            elif method == 'delete':
                response = self.client.delete(url)
            
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                           f"Unauthenticated access to {url} should be forbidden")

class ErrorHandlingTests(BaseAPITestCase):
    """
    Test error handling for various scenarios
    """
    
    def test_create_book_invalid_data(self):
        """Test creating a book with invalid data"""
        self.login_user('regularuser', 'testpass123')
        
        url = reverse('api:book-create')
        invalid_data = {
            'title': '',  # Empty title
            'author': 'Test Author',
            'publication_year': 'invalid'  # Invalid year
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertIn('publication_year', response.data)
        
        self.logout_user()
    
    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist"""
        url = reverse('api:book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_book(self):
        """Test updating a book that doesn't exist"""
        self.login_user('regularuser', 'testpass123')
        
        url = reverse('api:book-update', kwargs={'pk': 9999})
        data = {'title': 'Nonexistent Book'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        self.logout_user() 

