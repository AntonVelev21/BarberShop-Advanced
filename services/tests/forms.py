import os

import django
from django.test import TestCase

from services.forms import ServiceCreateForm, BarberCreateForm, ServiceEditForm, BarberEditForm
from services.models import Service, Barber

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber_shop.settings')
django.setup()


class ServiceFormTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Test',
            price=20,
            duration=40,
            description='Testing...',
            image_url='https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg'
        )

        self.valid_service_data = {
            'name': 'Test',
            'price': 30,
            'duration': 40,
            'description': 'Testing...',
            'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg'
        }

        self.invalid_service_data = {
            'name': 'Test',
            'price': -1,  # price is negative
            'duration': 40,
            'description': 'Testing...',
            'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg'
        }


    def test_service_create_with_valid_data(self):
        form = ServiceCreateForm(data=self.valid_service_data)
        self.assertTrue(form.is_valid())


    def test_service_create_with_invalid_data(self):
        form = ServiceCreateForm(data=self.invalid_service_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        self.assertEqual(
            form.errors['price'][0],
            'Price can not be negative!'
        )


    def test_service_create_with_missing_data(self):
        service_data = {
            'name': 'Test',
                            #price is missing
            'duration': 40,
            'description': 'Testing...',
            'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg'
        }
        form = ServiceCreateForm(data=service_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        self.assertEqual(
            form.errors['price'][0],
            'This field is required.'
        )


    def test_service_edit_with_valid_data(self):
        form = ServiceEditForm(data=self.valid_service_data, instance=self.service)
        self.assertTrue(form.is_valid())


    def test_service_edit_with_invalid_data(self):
        form = ServiceEditForm(data=self.invalid_service_data, instance=self.service)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        self.assertEqual(
            form.errors['price'][0],
            'Price can not be negative!'
        )



class BarberFormTests(TestCase):
    def setUp(self):
        self.barber = Barber.objects.create(
            first_name='Test',
            last_name='Example',
            image_url='https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
            bio='Lorem Ipson...',
            years_of_experience=4
        )

        self.valid_barber_data = {
            'first_name': 'Test',
            'last_name': 'Example',
            'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
            'bio': 'Lorem Ipson...',
            'years_of_experience': 5
        }

        self.invalid_barber_data = {
            'first_name': 'Test',
            'last_name': 'Example',
            'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
            'bio': 'Lorem Ipson...',
            'years_of_experience': -5  # years_of_experience is negative
        }


    def test_barber_create_with_valid_data(self):
        form = BarberCreateForm(data=self.valid_barber_data)
        self.assertTrue(form.is_valid())


    def test_barber_create_with_invalid_data(self):
        form = BarberCreateForm(data=self.invalid_barber_data)
        self.assertFalse(form.is_valid())
        self.assertIn('years_of_experience', form.errors)
        self.assertEqual(
            form.errors['years_of_experience'][0],
            'Barber experience can not be negative number!'
        )


    def test_barber_create_with_missing_data(self):
        barber_data_with_missing_field = {
            'first_name': 'Test',
            'last_name': 'Example',
            'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
            'bio': 'Lorem Ipson...',
                                        # years_of_experience is missing
        }

        form = BarberCreateForm(data=barber_data_with_missing_field)
        self.assertFalse(form.is_valid())
        self.assertIn('years_of_experience', form.errors)
        self.assertEqual(
            form.errors['years_of_experience'][0],
            'This field is required.'
        )


    def test_barber_edit_with_valid_data(self):
        form = BarberEditForm(data=self.valid_barber_data, instance=self.barber)
        self.assertTrue(form.is_valid())


    def test_barber_edit_with_invalid_data(self):
        form = BarberEditForm(data=self.invalid_barber_data, instance=self.barber)
        self.assertFalse(form.is_valid())
        self.assertIn('years_of_experience', form.errors)
        self.assertEqual(
            form.errors['years_of_experience'][0],
            'Barber experience can not be negative number!'
        )