import os

import django
from django.test import TestCase

from bookings.forms import BookingCreateForm, BookingEditForm
from bookings.models import Booking

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber_shop.settings')
django.setup()

from django.contrib.auth.models import User
from services.models import Barber, Service


class BookingFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_userr',
            password='test1234'
        )

        self.barber = Barber.objects.create(
            first_name='test3',
            last_name='test',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            bio='Test',
            years_of_experience=4,

        )

        self.service1 = Service.objects.create(
            name='Test1',
            price=5,
            duration=50,
            description='Test',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s'
        )

        self.service2 = Service.objects.create(
            name='Test2',
            price=56,
            duration=50,
            description='Test',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s'
        )

    def test_booking_create_with_valid_data(self):
        form_data = {
            'date_and_hour': '2026-04-15 14:30',
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_booking_create_with_invalid_hour(self):
        form_data_a = {
            'date_and_hour': '2026-04-15 14:35', #The hour is not in allowed hours (only between 00 and 30)
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form_a = BookingCreateForm(data=form_data_a)
        self.assertFalse(form_a.is_valid())

        form_data_b = {
            'date_and_hour': '2026-04-15 20:30', #The hour is not in working hours (09:00 - 20:00)
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form_b = BookingCreateForm(data=form_data_b)
        self.assertFalse(form_b.is_valid())


    def test_booking_create_with_rest_day(self):
        form_data = {
            'date_and_hour': '2026-04-19 14:30', #The day is not in working days (Monday - Saturday: 09:00 - 20:00)
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_booking_create_when_booking_on_the_date_and_hour_with_the_same_barber_exists(self):
        booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber,
            date_and_hour='2026-04-14 14:30'
        )

        form_data = {
            'date_and_hour': '2026-04-14 14:30', #The date_and_hour field is already used in other instance with the same barber
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_booking_edit_with_the_same_time_is_valid(self):
        booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber,
            date_and_hour='2026-04-15 14:30'
        )

        form_data = {
            'date_and_hour': '2026-04-15 14:30',
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingEditForm(data=form_data, instance=booking)

        if not form.is_valid():
            print(f"\nFORM ERRORS: {form.errors.as_json()}")
        self.assertTrue(form.is_valid())
