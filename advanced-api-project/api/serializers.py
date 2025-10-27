from rest_framework import serializers
from datetime import datetime
from .models import Author, Book 

# Serializer for the Book model
# This includes validation to ensure publication_year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Serializes all model fields (title, publication_year, author)

    def validate_publication_year(self, value):
        """Ensure the publication year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer for the Author model
# Includes a nested representation of books using the BookSerializer.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested relationship: show all books for the author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

    # Documentation note:
    # The 'books' field uses the related_name from the Book model ('books')
    # to automatically fetch and serialize all associated Book instances.