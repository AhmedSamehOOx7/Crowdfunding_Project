# Utility functions and helpers for accounts app
from django.utils.text import slugify


def generate_username_from_email(email):
    """Generate a unique username from email address"""
    local_part = email.split('@')[0]
    base_username = slugify(local_part)
    username = base_username
    counter = 1
    from .models import User
    while User.objects.filter(username=username).exists():
        username = f"{base_username}-{counter}"
        counter += 1
    return username
