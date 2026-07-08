from rest_framework import serializers
from django.db import transaction
from .models import Category, Campaign, CampaignImage, Donation
from accounts.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.IntegerField(source='get_progress_percentage', read_only=True)
    days_left = serializers.IntegerField(source='get_days_left', read_only=True)
    donor_count = serializers.IntegerField(source='get_donor_count', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ['owner', 'raised_amount', 'created_at', 'updated_at']


class CampaignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignImage
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'donor', 'campaign', 'amount', 'donated_at']
        read_only_fields = ['donor', 'campaign', 'donated_at']

    def validate(self, attrs):
        user = self.context.get('request').user
        campaign = self.context.get('campaign')

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to donate.")
        if campaign and campaign.owner == user:
            raise serializers.ValidationError("You cannot donate to your own campaign.")
        if attrs.get('amount', 0) <= 0:
            raise serializers.ValidationError("Donation amount must be greater than zero.")

        return attrs

    def create(self, validated_data):
        campaign = self.context.get('campaign')
        user = self.context.get('request').user
        with transaction.atomic():
            donation = Donation.objects.create(
                donor=user,
                campaign=campaign,
                **validated_data
            )
        return donation
