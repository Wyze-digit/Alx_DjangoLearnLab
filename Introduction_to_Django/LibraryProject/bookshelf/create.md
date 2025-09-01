# file created for placeholder
# Create a Book

```python
from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
book  # Expected (example): <Book: 1984 by George Orwell (1949)>

