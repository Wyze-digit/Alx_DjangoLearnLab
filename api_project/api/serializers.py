# api/serializers.py

from rest_framework import serializers
from .models import Book
from .models import Item

class BookSerializer(serializers.ModelSerializer):
    """Serializer to convert Book model instances into JSON format."""
    
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields of the Book model  

# api/serializers.py
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'