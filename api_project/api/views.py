from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Item
from .serializers import ItemSerializer



class BookList(generics.ListAPIView):
#    """API view to list all books in the database."""
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Example ViewSet secured with authentication
class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    Authentication & Permission enforced using DRF classes.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # Only authenticated users can access this endpoint
    permission_classes = [IsAuthenticated]

# Example of role-based or admin-only access
class AdminItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows only admins to manage items.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # Only admin users can access this endpoint
    permission_classes = [IsAdminUser]

# Optional: Example of a public endpoint (no authentication required)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_info(request):
    """
    A public endpoint accessible without authentication.
    """
    return Response({"message": "Welcome to the public API endpoint!"})
