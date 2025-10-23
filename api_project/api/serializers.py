# api/serializers.py

from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer to convert Book model instances into JSON format."""
    
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields of the Book model