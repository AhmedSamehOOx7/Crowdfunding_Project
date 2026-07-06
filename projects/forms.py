from django import forms
from django.core.exceptions import ValidationError
from .models import Campaign, CampaignImage, Donation


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'short_description', 'story', 'category', 'goal_amount', 'start_date', 'end_date', 'cover_image']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


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
