# api/urls.py
from . import views
from .views import BookList 
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from .views import BookViewSet
from .views import BookViewSet




# Create a router and register our ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')
router.register(r'items', views.ItemViewSet, basename='item') # itemviewset registration
router.register(r'admin-items', views.AdminItemViewSet, basename='admin-item')


urlpatterns = [
    path('', include(router.urls)),
    path('public/', views.public_info, name='public-info'),
    path('books/', BookList.as_view(), name='book-list'), 
]

