## `LibraryProject/bookshelf/update.md`
```markdown
# Update the Book Title

```python
from bookshelf.models import Book

# Update the title and save
b = Book.objects.get(title="1984", author="George Orwell")
b.title = "Nineteen Eighty-Four"
b.save()
(b.id, b.title, b.author, b.publication_year)  # Expected (example): (1, "Nineteen Eighty-Four", "George Orwell", 1949)
