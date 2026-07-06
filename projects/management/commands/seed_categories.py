from django.core.management.base import BaseCommand
from projects.models import Category


class Command(BaseCommand):
    help = 'Seed initial categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Medical', 'slug': 'medical', 'icon': 'fa-heart-pulse'},
            {'name': 'Education', 'slug': 'education', 'icon': 'fa-graduation-cap'},
            {'name': 'Technology', 'slug': 'technology', 'icon': 'fa-microchip'},
            {'name': 'Charity', 'slug': 'charity', 'icon': 'fa-hands-holding-child'},
            {'name': 'Startup', 'slug': 'startup', 'icon': 'fa-rocket'},
            {'name': 'Community', 'slug': 'community', 'icon': 'fa-users'},
            {'name': 'Environment', 'slug': 'environment', 'icon': 'fa-leaf'},
        ]

        for category_data in categories:
            category, created = Category.objects.get_or_create(
                slug=category_data['slug'],
                defaults=category_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                self.stdout.write(f"Category already exists: {category.name}")
