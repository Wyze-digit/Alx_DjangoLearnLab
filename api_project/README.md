Django REST Framework API Setup

This project demonstrates the setup of a basic Django REST Framework (DRF) API for listing books. It’s part of the foundational work for developing RESTful APIs using Django.

🚀 Project Overview

This project introduces:

Installation and setup of Django REST Framework

Creation of a simple Book model

Implementation of serializers, API views, and routing

Exposure of an API endpoint (/api/books/) that returns all book records in JSON format

Project Structure
api_project/
│
├── api_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
└── manage.py

⚙️ Setup Instructions
1️⃣ Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows

2️⃣ Install Dependencies
pip install django djangorestframework

3️⃣ Start a New Project and App
django-admin startproject api_project
cd api_project
python manage.py startapp api

4️⃣ Update settings.py

Add the following apps:

INSTALLED_APPS = [
    ...
    'rest_framework',
    'api',
]

🧩 Implementation Details
🧾 Book Model (api/models.py)

Defines a simple Book model with title and author fields.

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.title

🔄 Serializer (api/serializers.py)

Converts model instances into JSON.

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

👀 View (api/views.py)

Uses Django REST Framework’s ListAPIView to retrieve all books.

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

🌐 URL Routing

App-level api/urls.py:

from django.urls import path
from .views import BookList

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
]


Project-level api_project/urls.py:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

🧪 Testing the API

Apply migrations:

python manage.py makemigrations
python manage.py migrate


Run the server:

python manage.py runserver


Visit:

http://127.0.0.1:8000/api/books/


If books exist, you’ll see a JSON response similar to:

[
  {
    "id": 1,
    "title": "Django for Beginners",
    "author": "William S. Vincent"
  },
  {
    "id": 2,
    "title": "Python Crash Course",
    "author": "Eric Matthes"
  }
]

🛡️ Notes

The API uses Django REST Framework’s built-in security and serialization features.

This setup lays the foundation for future CRUD operations (Create, Retrieve, Update, Delete).