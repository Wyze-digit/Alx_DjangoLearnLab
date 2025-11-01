# blog/templatetags/blog_extras.py
from django import template

register = template.Library()

@register.filter
def truncate_chars(value, max_length):
    """Truncate text to specified number of characters"""
    if len(value) <= max_length:
        return value
    return value[:max_length-3] + '...'

@register.simple_tag
def recent_posts(count=5):
    """Get recent published posts"""
    from blog.models import Post
    return Post.objects.filter(status='published')[:count]  

