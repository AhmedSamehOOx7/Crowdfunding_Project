from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Campaign, CampaignImage, Donation


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'short_description', 'story', 'category', 'goal_amount', 'start_date', 'end_date', 'cover_image']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['short_description'].required = True
        self.fields['story'].required = True
        self.fields['category'].required = True
        self.fields['goal_amount'].required = True
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['cover_image'].required = True

    def clean_goal_amount(self):
        amount = self.cleaned_data.get('goal_amount')
        if amount <= 0:
            raise ValidationError("Goal amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date.")
            if end_date <= timezone.now().date():
                raise ValidationError("End date must be in the future.")

        return cleaned_data


class CampaignImageForm(forms.ModelForm):
    class Meta:
        model = CampaignImage
        fields = ['image', 'caption']


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'min': 0.01, 
                'step': 0.01, 
                'class': 'form-control',
                'placeholder': 'Enter amount in EGP'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        self.campaign = kwargs.pop('campaign', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        
        if not self.user or not self.user.is_authenticated:
            raise ValidationError("You must be logged in to donate.")
            
        if self.campaign and self.campaign.owner == self.user:
            raise ValidationError("You cannot donate to your own campaign.")
            
        if amount and amount <= 0:
            raise ValidationError("Donation amount must be greater than zero.")
            
        return cleaned_data
