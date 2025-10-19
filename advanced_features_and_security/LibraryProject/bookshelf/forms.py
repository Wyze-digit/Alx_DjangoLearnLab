from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """
    ExampleForm
    ------------
    This form is connected to the Book model and allows creating or editing
    book instances securely. It demonstrates Django’s built-in form validation,
    automatic CSRF protection in templates, and integration with model fields.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'description']

        # Optional: Add basic widgets for styling and better input handling
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ISBN number'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }

        # Optional: Add labels for clarity
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'published_date': 'Publication Date',
            'isbn': 'ISBN',
            'description': 'Description',
        }
        