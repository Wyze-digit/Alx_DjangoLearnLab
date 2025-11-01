from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Category

def home(request):
    """Home page with recent published posts"""
    recent_posts = Post.objects.filter(status='published').select_related('author')[:5]
    context = {
        'posts': recent_posts,
        'featured_posts': recent_posts[:3] if recent_posts else []
    }
    return render(request, 'blog/home.html', context)

def post_list(request):
    """List all published posts with PostgreSQL optimization"""
    posts = Post.objects.filter(status='published').select_related('author').prefetch_related('categories')
    context = {'posts': posts}
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    """Individual post detail view"""
    post = get_object_or_404(Post.objects.select_related('author'), slug=slug, status='published')
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, slug):
    """View to display posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        status='published', 
        categories__category=category
    ).select_related('author')
    
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/category_posts.html', context)

@login_required
def post_create(request):
    """Create new post (placeholder for now)"""
    return render(request, 'blog/post_create.html')  

