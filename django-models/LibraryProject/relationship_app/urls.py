# this file is created to solve the url viewing issues. 
# 

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books 


urlpatterns = [
    # Function-Based Views (FBV)
    path("books/", views.list_books, name="list_books"),
    path("libraries/<int:pk>/", views.library_detail, name="library_detail"),

    # Class-Based Views (CBV)
    path("books-class/", views.BookListView.as_view(), name="book_list_class"),
    path("libraries-class/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail_class"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),  # optional homepage
]

urlpatterns = [
    # Registration view
    path('register/', views.register, name='register'),

    # Login view using Django built-in authentication
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout view using Django built-in authentication
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]

