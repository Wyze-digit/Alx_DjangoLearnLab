

# Create your views here.
from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all()   # <-- required query
    return render(request, "relationship_app/list_books.html", {"books": books})  # <-- required template


# others
from django.shortcuts import render, get_object_or_404
from .models import Library 

from django.views.generic.detail import DetailView

def library_detail(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    return render(request, 'relationship_app/library_detail.html', {'library': library})

# relationship_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

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