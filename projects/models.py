from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Campaign(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    story = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='campaigns')
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()
    cover_image = models.ImageField(upload_to='campaign_covers/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_progress_percentage(self):
        if self.goal_amount == 0:
            return 0
        try:
            percentage = (float(self.raised_amount) / float(self.goal_amount)) * 100
            return round(min(100, percentage))
        except (ZeroDivisionError, TypeError):
            return 0

    def get_days_left(self):
        today = date.today()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days

    def get_donor_count(self):
        return self.donations.values('donor').distinct().count()


class CampaignImage(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='campaign_gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.campaign.title}"


class Donation(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-donated_at']

    def __str__(self):
        return f"{self.donor.username} donated {self.amount} to {self.campaign.title}"
