#

import os
import django

# Setup Django environment (only needed if run as standalone script)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_pro.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def run_queries():
    # Create sample data
    author = Author.objects.create(name="George Orwell")
    book1 = Book.objects.create(title="1984", author=author)
    book2 = Book.objects.create(title="Animal Farm", author=author)

    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2)

    librarian = Librarian.objects.create(name="Alice", library=library)

    # Query 1: All books by a specific author
    print("\nBooks by George Orwell:")
    for book in author.books.all():
        print(f"- {book.title}")

    # Query 2: List all books in a library
    print("\nBooks in Central Library:")
    for book in library.books.all():
        print(f"- {book.title}")

    # Query 3: Retrieve the librarian for a library
    print("\nLibrarian of Central Library:")
    print(library.librarian.name)


if __name__ == "__main__":
    run_queries()
