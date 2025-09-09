# CRUD Operations on Book Model

## Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book

#sample output is shown below:
# <Book: 1984 by George Orwell (1949)>


# this block of code is for retrieve
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year

# this is expected output
# ('1984', 'George Orwell', 1949)

#this block of code is for update
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
#output sample
# <Book: Nineteen Eighty-Four by George Orwell (1949)>

# this block of code is for delete
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# sample output below
# <QuerySet []>




