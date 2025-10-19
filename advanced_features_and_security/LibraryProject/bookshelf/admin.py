# Register your models here.
from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Customize how Book model appears in the admin
# class BookAdmin(admin.ModelAdmin):
#    list_display = ('title', 'author', 'publication_year')   # columns shown in list view
#    list_filter = ('publication_year', 'author')             # sidebar filters
#    search_fields = ('title', 'author')                      # search functionality

# Create BookAdmin Class
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'publication_year')
#     list_filter = ('publication_year', 'author')
#     search_fields = ('title', 'author') 

# Register Book model with its custom admin configuration
# admin.site.register(Book, BookAdmin) 

# -------------------------
# Custom User Admin
# -------------------------
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "date_of_birth", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )

# Important: Register your custom model and admin class
admin.site.register(CustomUser, CustomUserAdmin)

