import os
import django
from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import UserProfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber_shop.settings')
django.setup()


class UserProfileTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='Test',
            password='Tonini2003'
        )
    def test_user_profile_creates_successfully_with_signal(self):
        self.assertTrue(UserProfile.objects.filter(user=self.test_user).exists())

    def test_user_profile_does_not_duplicate_on_user_update(self):
        self.test_user.first_name = 'Pesho'
        self.test_user.save()
        self.assertEqual(UserProfile.objects.filter(user=self.test_user).count(), 1)

    def test_user_profile_deletes_successfully(self):
        self.test_user.delete()
        self.assertFalse(UserProfile.objects.filter(user__username='Test').exists())