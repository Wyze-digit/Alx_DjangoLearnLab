from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Category

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm

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

"""
new codes

"""  
def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'blog/register.html', context)

def custom_login(request):
    """Custom login view with messages"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next page if provided, otherwise home
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'blog/login.html', context)

def custom_logout(request):
    """Custom logout view with message"""
    if request.user.is_authenticated:
        messages.info(request, 'You have been successfully logged out.')
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    """User profile management view"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'blog/profile.html', context)