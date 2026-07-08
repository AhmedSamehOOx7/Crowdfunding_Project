from django.contrib import admin
from .models import Category, Campaign, CampaignImage, Donation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class CampaignImageInline(admin.TabularInline):
    model = CampaignImage
    extra = 1


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'goal_amount', 'raised_amount', 'start_date', 'end_date', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'category', 'created_at', 'start_date', 'end_date')
    search_fields = ('title', 'short_description', 'story', 'owner__username', 'owner__email')
    prepopulated_fields = {}  # If we had a slug, we'd use it
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [CampaignImageInline]


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'campaign', 'amount', 'donated_at')
    list_filter = ('donated_at',)
    search_fields = ('donor__username', 'donor__email', 'campaign__title')
    date_hierarchy = 'donated_at'
    ordering = ('-donated_at',)
