# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post-list'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('post/new/', views.post_create, name='post-create'),
    path('category/<slug:slug>/', views.category_posts, name='category-posts'),
]
