

# Create your views here.
from django.shortcuts import render
from .models import Book 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Library 
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages


def list_books(request):
    books = Book.objects.all()   # <-- required query
    return render(request, "relationship_app/list_books.html", {"books": books})  # <-- required template


# others
def library_detail(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    return render(request, 'relationship_app/library_detail.html', {'library': library})

# relationship_app/views.py
# -------------------------------
# Register View
# -------------------------------
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# -------------------------------
# Login View
# -------------------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # You can define a homepage or dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


# -------------------------------
# Logout View
# -------------------------------
@login_required
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')


# -------------------------------
# Example Home Page (For Testing)
# -------------------------------
@login_required
def home_view(request):
    return render(request, 'relationship_app/home.html', {'user': request.user}) 

# -----------------------------------
# Role check functions 
# ----------------------------------- 
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# --------------------------------
# add checks before your views
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin' 

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian' 
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member' 

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# ----------------------------------------------
# View to add a book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('book_list')
    return render(request, 'relationship_app/add_book.html')

# ----------------------------------------
# View to edit a book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_date = request.POST.get('published_date')
        book.save()
        return redirect('book_list')
    return render(request, 'relationship_app/edit_book.html', {'book': book})

# ------------------------------------------
# View to delete a book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# ------------------------------------------
# Optional view to list books (for navigation/testing)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})




# Views 
# --------------------------
# @login_required
# @user_passes_test(is_admin)
# def admin_view(request):
#     return render(request, 'admin_view.html')
# 
# @login_required
# @user_passes_test(is_librarian)
# def librarian_view(request):
#     return render(request, 'librarian_view.html')
# 
# @login_required
# @user_passes_test(is_member)
# def member_view(request):
#     return render(request, 'member_view.html')