# blog/context_processors.py
from .models import Category

def blog_context(request):
    """Global context available to all templates"""
    return {
        'all_categories': Category.objects.all(),
        'current_year': 2024,
    }
