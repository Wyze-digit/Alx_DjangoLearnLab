from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    """
    Blog Post model with PostgreSQL-specific features
    """
    title = models.CharField(max_length=200, db_index=True)  # Index for faster searches
    slug = models.SlugField(max_length=200, unique=True, db_index=True)  # SEO-friendly URLs
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)  # Short description
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),  # PostgreSQL index for ordering
            models.Index(fields=['status', 'published_date']),  # Composite index
        ]
        db_table = 'blog_posts'  # Explicit table name
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            self.excerpt = self.content[:297] + '...' if len(self.content) > 300 else self.content
        super().save(*args, **kwargs)

class Category(models.Model):
    """
    Category model for organizing posts
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class PostCategory(models.Model):
    """
    Many-to-Many relationship between Post and Category
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'blog_post_categories'
        unique_together = ['post', 'category'] 


