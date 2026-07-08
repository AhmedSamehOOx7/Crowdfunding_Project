from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Campaign, Category, Donation
from .forms import DonationForm
from django.urls import reverse

User = get_user_model()


class CampaignModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            mobile_phone='01012345678'
        )
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.campaign = Campaign.objects.create(
            owner=self.user,
            title='Test Campaign',
            short_description='Test short desc',
            story='Test story',
            category=self.category,
            goal_amount=1000.00,
            raised_amount=0.00,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            cover_image='test.jpg'
        )

    def test_progress_percentage_0_percent(self):
        self.campaign.raised_amount = 0.00
        self.campaign.goal_amount = 1000.00
        self.assertEqual(self.campaign.get_progress_percentage(), 0)

    def test_progress_percentage_50_percent(self):
        self.campaign.raised_amount = 500.00
        self.campaign.goal_amount = 1000.00
        self.assertEqual(self.campaign.get_progress_percentage(), 50)

    def test_progress_percentage_overflow(self):
        self.campaign.raised_amount = 1500.00
        self.campaign.goal_amount = 1000.00
        self.assertEqual(self.campaign.get_progress_percentage(), 100)

    def test_get_days_left_active(self):
        self.assertGreater(self.campaign.get_days_left(), 0)

    def test_get_days_left_expired(self):
        self.campaign.end_date = timezone.now().date() - timedelta(days=1)
        self.campaign.save()
        self.assertEqual(self.campaign.get_days_left(), 0)

    def test_get_donor_count_unique(self):
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test2',
            last_name='User2',
            mobile_phone='01098765432'
        )
        Donation.objects.create(donor=self.user, campaign=self.campaign, amount=100)
        Donation.objects.create(donor=self.user, campaign=self.campaign, amount=200)
        Donation.objects.create(donor=user2, campaign=self.campaign, amount=150)
        self.assertEqual(self.campaign.get_donor_count(), 2)


class DonationFormTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123',
            first_name='Owner',
            last_name='User',
            mobile_phone='01012345678'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            mobile_phone='01098765432'
        )
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.campaign = Campaign.objects.create(
            owner=self.owner,
            title='Test Campaign',
            short_description='Test short desc',
            story='Test story',
            category=self.category,
            goal_amount=1000.00,
            raised_amount=0.00,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            cover_image='test.jpg'
        )

    def test_form_rejects_owner_donation(self):
        form_data = {'amount': 100}
        form = DonationForm(data=form_data, campaign=self.campaign, user=self.owner)
        self.assertFalse(form.is_valid())

    def test_form_rejects_zero_amount(self):
        form_data = {'amount': 0}
        form = DonationForm(data=form_data, campaign=self.campaign, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_rejects_negative_amount(self):
        form_data = {'amount': -50}
        form = DonationForm(data=form_data, campaign=self.campaign, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_accepts_valid_donation(self):
        form_data = {'amount': 100}
        form = DonationForm(data=form_data, campaign=self.campaign, user=self.user)
        self.assertTrue(form.is_valid())


class CampaignViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123',
            first_name='Owner',
            last_name='User',
            mobile_phone='01012345678'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            mobile_phone='01098765432'
        )
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.campaign = Campaign.objects.create(
            owner=self.owner,
            title='Test Campaign',
            short_description='Test short desc',
            story='Test story',
            category=self.category,
            goal_amount=1000.00,
            raised_amount=0.00,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            cover_image='test.jpg'
        )

    def test_successful_donation_updates_raised_amount(self):
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(
            reverse('campaign_detail', kwargs={'pk': self.campaign.pk}),
            {'amount': 100}
        )
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.raised_amount, 100.00)
