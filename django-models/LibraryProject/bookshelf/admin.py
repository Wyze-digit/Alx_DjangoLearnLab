from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book

# Customize how Book model appears in the admin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # columns shown in list view
    list_filter = ('publication_year', 'author')             # sidebar filters
    search_fields = ('title', 'author')                      # search functionality

# Create BookAdmin Class
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author') 

# Register Book model with its custom admin configuration
admin.site.register(Book, BookAdmin) 



