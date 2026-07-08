from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Donation, Campaign


@receiver(post_save, sender=Donation)
def update_campaign_raised_amount(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            campaign = Campaign.objects.select_for_update().get(pk=instance.campaign.pk)
            campaign.raised_amount += instance.amount
            campaign.save(update_fields=['raised_amount'])
