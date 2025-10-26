from django.db import models
from datetime import datetime 


# Create your models here.
# The Author model represents a writer in the system.
# Each Author can have multiple Books (one-to-many relationship).
class Author(models.Model):
    """
    Author model represents a writer in the system.
    Fields:
        name (CharField): The name of the author.
    """
    name = models.CharField(max_length=100,help_text="Enter the author's full name")

    def __str__(self):
        return self.name


# The Book model represents a single book written by an Author.
# It includes the title, publication year, and a foreign key linking to Author.
class Book(models.Model):
    """
    Book model represents a book written by an author.
    Fields:
        title (CharField): Title of the book.
        publication_year (IntegerField): Year the book was published.
        author (ForeignKey): Links each book to its author (one-to-many relationship).
    """
    title = models.CharField(max_length=200, help_text="Enter the book title")
    publication_year = models.IntegerField(help_text="Enter the year the bood was published")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"