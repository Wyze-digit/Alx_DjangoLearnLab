# this file is created to solve the url viewing issues. 
# 

# from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
# from . import views
# from .views import list_books 
# urlpatterns = [
    # Function-Based Views (FBV)
#    path("books/", views.list_books, name="list_books"),
#    path("libraries/<int:pk>/", views.library_detail, name="library_detail"),

#    # Class-Based Views (CBV)
#    path("books-class/", views.BookListView.as_view(), name="book_list_class"),
#    path("libraries-class/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail_class"),
# ]
#
# from django.urls import path
# from . import views
#
# urlpatterns = [
#    path('register/', views.register_view, name='register'),
#    path('login/', views.login_view, name='login'),
#    path('logout/', views.logout_view, name='logout'),
#    path('', views.home_view, name='home'),  # optional homepage
# ]
#
# urlpatterns = [
#    # Registration view
#    path('register/', views.register, name='register'),
#
#    # Login view using Django built-in authentication
#    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
#
#    # Logout view using Django built-in authentication
#    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
# ]

# relationship_app/urls.py
# This file defines all URL routes for the relationship_app, including
# books, libraries, and user authentication.

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # -------------------------------
    # Function-Based Views (FBV)
    # -------------------------------
    path("books/", views.list_books, name="list_books"),
    path("libraries/<int:pk>/", views.library_detail, name="library_detail"),

    # -------------------------------
    # Class-Based Views (CBV)
    # -------------------------------
    path("books-class/", views.BookListView.as_view(), name="book_list_class"),
    path("libraries-class/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail_class"),

    # -------------------------------
    # User Authentication URLs
    # -------------------------------
    # Registration view
    path("register/", views.register, name="register"),

    # Login view using Django built-in authentication
    path(
        "login/",
        LoginView.as_view(template_name="relationship_app/login.html"),
        name="login"
    ),

    # Logout view using Django built-in authentication
    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout"
    ),

    # -------------------------------
    # Optional Homepage
    # -------------------------------
    path("", views.home_view, name="home"),

    # --------------------------------
    # user-role views 
    # --------------------------------
    # path('admin/dashboard/', views.admin_view, name='admin_view'),
    # path('librarian/dashboard/', views.librarian_view, name='librarian_view'),
    # path('member/dashboard/', views.member_view, name='member_view'),

    # Role-based access views
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
    path('books/', views.book_list, name='book_list'),
    # path('books/add/', views.add_book, name='add_book'),
    # path('books/edit/<int:id>/', views.edit_book, name='edit_book'),
    # path('books/delete/<int:id>/', views.delete_book, name='delete_book'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:id>/', views.delete_book, name='delete_book'),
    path('books/', views.book_list, name='book_list'),

]


