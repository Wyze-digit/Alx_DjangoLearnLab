from django.contrib import admin

# Register your models here.
from .models import Author, Book 

# Inline display of Books under Author in the admin interface.
class BookInline(admin.TabularInline):
    model = Book
    extra = 1  # Number of empty book forms to display by default


# Custom admin view for Author with nested Book management
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [BookInline]


# Custom admin view for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_year', 'author')
    list_filter = ('publication_year', 'author')
    search_fields = ('title',)