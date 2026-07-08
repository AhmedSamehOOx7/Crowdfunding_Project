# Utility functions and helpers for projects app
from django.utils import timezone


def is_campaign_active(campaign):
    """Check if a campaign is currently active (between start and end date)"""
    today = timezone.now().date()
    return campaign.start_date <= today <= campaign.end_date


def calculate_campaign_metrics(campaign):
    """Calculate various campaign metrics"""
    total_raised = campaign.raised_amount
    percentage = campaign.get_progress_percentage()
    days_left = campaign.get_days_left()
    remaining = max(0, campaign.goal_amount - total_raised)
    return {
        'total_raised': total_raised,
        'percentage': percentage,
        'days_left': days_left,
        'remaining': remaining
    }
