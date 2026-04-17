from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import CustomUserCreationForm


class CustomUserCreationFormTests(TestCase):
    def test_form_is_valid_with_not_existing_email(self):
        data = {
            'username': 'newuser',
            'email': 'unique@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())


    def test_form_invalid_when_email_exists(self):
        user = User.objects.create_user(
            username='Test',
            password='Test Test',
            email='duplicate@example.com'
        )

        data = {
            'username': 'newuser',
            'email': 'duplicate@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }

        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(
            form.errors['email'][0],
            'A user with that email already exists.'
        )


    def test_form_invalid_with_missing_email(self):
        data = {
            'username': 'newuser',
                                        #The email is missing
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(
            form.errors['email'][0],
            'This field is required.'
        )