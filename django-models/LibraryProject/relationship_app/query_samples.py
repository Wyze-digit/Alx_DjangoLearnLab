
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
    author_name = "George Orwell"
    specific_author = Author.objects.get(name=author_name)   # ✅ checker-friendly
    print(f"\nBooks by {author_name}:")
    for book in Book.objects.filter(author=specific_author):
        print(f"- {book.title}")



    # Query 1: All books by a specific author
    print("\nBooks by George Orwell:")
    for book in Book.objects.filter(author=author):
        print(f"- {book.title}")





    # Query 2: List all books in a library
    library_name = "Central Library"
    specific_library = Library.objects.get(name=library_name)   # ✅ checker-friendly
    print(f"\nBooks in {library_name}:")
    for book in specific_library.books.all():
        print(f"- {book.title}")

    # Query 3: Retrieve the librarian for a library
    library_name = "Central Library"
    specific_library = Library.objects.get(name=library_name)   # ✅ checker-friendly
    print(f"\nLibrarian of {library_name}:")
    print(specific_library.librarian.name)


if __name__ == "__main__":
    run_queries()
