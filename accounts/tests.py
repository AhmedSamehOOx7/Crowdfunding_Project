from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import User
from projects.models import Campaign, Category, Donation
from django.utils import timezone
from datetime import timedelta


class UserRegistrationTests(TestCase):
    def test_valid_egyptian_mobile_phone(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'mobile_phone': '01012345678'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_invalid_mobile_phone(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test2@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'mobile_phone': '123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='test2@example.com').exists())


class UserLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            mobile_phone='01012345678'
        )

    def test_login_with_email(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            mobile_phone='01012345678'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123',
            first_name='Other',
            last_name='User',
            mobile_phone='01098765432'
        )
        self.category = Category.objects.create(name='Test', slug='test')

        # Create user's campaign
        self.campaign = Campaign.objects.create(
            owner=self.user,
            title='Test Campaign',
            short_description='Test short desc',
            story='Test story',
            category=self.category,
            goal_amount=1000,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            cover_image='test.jpg'
        )

        # Create other user's campaign
        self.other_campaign = Campaign.objects.create(
            owner=self.other_user,
            title='Other Campaign',
            short_description='Other short desc',
            story='Other story',
            category=self.category,
            goal_amount=1000,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            cover_image='other.jpg'
        )

        # Create donation from user to other's campaign
        Donation.objects.create(
            donor=self.user,
            campaign=self.other_campaign,
            amount=100
        )

    def test_profile_view_only_user_own_campaigns_and_donations(self):
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        # Check if only user's campaigns are present
        self.assertContains(response, self.campaign.title)
        self.assertNotContains(response, self.other_campaign.title)

        # Check if user's donations are present
        self.assertContains(response, self.other_campaign.title)
