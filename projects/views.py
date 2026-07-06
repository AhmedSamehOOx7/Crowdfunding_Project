from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime
from .models import Campaign, Category, Donation
from .forms import CampaignForm, DonationForm


def home(request):
    featured_campaigns = Campaign.objects.filter(is_featured=True)[:3]
    latest_campaigns = Campaign.objects.order_by('-created_at')[:6]
    categories = Category.objects.all()
    top_campaigns = Campaign.objects.annotate(
        total_raised=Sum('donations__amount')
    ).order_by('-total_raised')[:4]
    return render(request, 'projects/home.html', {
        'featured_campaigns': featured_campaigns,
        'latest_campaigns': latest_campaigns,
        'categories': categories,
        'top_campaigns': top_campaigns,
    })


def campaign_list(request):
    campaigns = Campaign.objects.all()
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    filter_by = request.GET.get('filter')

    if query:
        campaigns = campaigns.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(story__icontains=query)
        )

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        campaigns = campaigns.filter(category=category)

    if filter_by == 'newest':
        campaigns = campaigns.order_by('-created_at')
    elif filter_by == 'most_funded':
        campaigns = campaigns.annotate(total_raised=Sum('donations__amount')).order_by('-total_raised')
    elif filter_by == 'ending_soon':
        campaigns = campaigns.order_by('end_date')

    categories = Category.objects.all()
    return render(request, 'projects/campaign_list.html', {
        'campaigns': campaigns,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
        'filter_by': filter_by,
    })


def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    donations = Donation.objects.filter(campaign=campaign)[:10]
    
    # Calculate campaign statistics
    total_raised = campaign.raised_amount
    number_of_donors = campaign.get_donor_count()
    funding_percentage = campaign.get_progress_percentage()
    remaining_amount = max(0, campaign.goal_amount - total_raised)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = DonationForm(request.POST, campaign=campaign, user=request.user)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.campaign = campaign
            donation.save()
            
            # Update campaign raised amount
            campaign.raised_amount += amount
            campaign.save()
            
            messages.success(request, "Thank you for your donation!")
            return redirect('campaign_detail', pk=campaign.pk)
    else:
        form = DonationForm(campaign=campaign, user=request.user)
        
    return render(request, 'projects/campaign_detail.html', {
        'campaign': campaign,
        'donations': donations,
        'form': form,
        'total_raised': total_raised,
        'number_of_donors': number_of_donors,
        'funding_percentage': funding_percentage,
        'remaining_amount': remaining_amount,
    })


@login_required
def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.owner = request.user
            campaign.save()
            messages.success(request, 'Campaign created successfully!')
            return redirect('campaign_detail', pk=campaign.pk)
    else:
        form = CampaignForm()
    categories = Category.objects.all()
    return render(request, 'projects/campaign_form.html', {'form': form, 'categories': categories})


@login_required
def campaign_edit(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.user != campaign.owner:
        messages.error(request, 'You are not authorized to edit this campaign.')
        return redirect('campaign_detail', pk=pk)
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign updated successfully!')
            return redirect('campaign_detail', pk=pk)
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'projects/campaign_form.html', {'form': form, 'campaign': campaign})


@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.user != campaign.owner:
        messages.error(request, 'You are not authorized to delete this campaign.')
        return redirect('campaign_detail', pk=pk)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, 'Campaign deleted successfully!')
        return redirect('profile')
    return render(request, 'projects/campaign_confirm_delete.html', {'campaign': campaign})


@login_required
def dashboard(request):
    user = request.user
    campaigns = Campaign.objects.filter(owner=user)
    donations = Donation.objects.filter(donor=user)
    return render(request, 'projects/dashboard.html', {
        'campaigns': campaigns,
        'donations': donations,
    })
