from datetime import datetime, timedelta
import os
from time import strftime

import django
from celery.utils.time import weekday
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

        now = datetime.now()
        if now.weekday() == 6:
            now = timedelta(days=1) + now
        self.valid_time_and_date = now.replace(year=now.year, month=now.month, day=now.day, hour=14, minute=30)
        self.formated_now = now.strftime("%Y-%m-%d %H:%M")

        self.formated_now_with_invalid_hour = self.valid_time_and_date.replace(minute=35).strftime("%Y-%m-%d %H:%M")
        self.formated_now_with_hour_outside_of_work_hours = self.valid_time_and_date.replace(hour=21).strftime("%Y-%m-%d %H:%M")
        days_until_sunday = 7 - self.valid_time_and_date.isoweekday()
        self.formated_now_with_day_outside_of_work_days = (self.valid_time_and_date + timedelta(days_until_sunday)).strftime("%Y-%m-%d %H:%M")


    def test_booking_create_with_valid_data(self):
        form_data = {
            'date_and_hour': self.valid_time_and_date,
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_booking_create_with_invalid_hour(self):
        form_data_a = {
            'date_and_hour': self.formated_now_with_invalid_hour, #The hour is not in allowed hours (only between 00 and 30)
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form_a = BookingCreateForm(data=form_data_a)
        self.assertFalse(form_a.is_valid())
        self.assertIn('date_and_hour', form_a.errors)
        self.assertEqual(
            form_a.errors['date_and_hour'][0],
            'Please select a valid time slot (e.g. 10:00 or 10:30).'
        )

        form_data_b = {
            'date_and_hour': self.formated_now_with_hour_outside_of_work_hours, #The hour is not in working hours (09:00 - 20:00)
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form_b = BookingCreateForm(data=form_data_b)
        self.assertFalse(form_b.is_valid())
        self.assertIn('date_and_hour', form_b.errors)
        self.assertEqual(
            form_b.errors['date_and_hour'][0],
            'Our working hours are between 09:00 and 18:00.'
        )


    def test_booking_create_with_rest_day(self):
        form_data = {
            'date_and_hour': self.formated_now_with_day_outside_of_work_days, #The day is not in working days (Monday - Saturday: 09:00 - 20:00)
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_and_hour', form.errors)
        self.assertEqual(
            form.errors['date_and_hour'][0],
            'Please choose a working day. We work from Monday to Saturday.'
        )

    def test_booking_create_in_the_past(self):
        form_data = {
            'date_and_hour': '2026-04-04 14:30',
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }
        form = BookingCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_and_hour', form.errors)
        self.assertEqual(
            form.errors['date_and_hour'][0],
            'You cannot book a seat in the past!'
        )

    def test_booking_create_when_booking_on_the_date_and_hour_with_the_same_barber_exists(self):
        booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber,
            date_and_hour=self.valid_time_and_date
        )

        form_data = {
            'date_and_hour': self.valid_time_and_date, #The date_and_hour field is already used in other instance with the same barber
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_and_hour', form.errors)
        self.assertEqual(
            form.errors['date_and_hour'][0],
            'Sorry, test3 is already booked for this time. Please choose another.'
        )


    def test_booking_edit_with_the_same_time_is_valid(self):
        booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber,
            date_and_hour=self.valid_time_and_date
        )

        form_data = {
            'date_and_hour': self.valid_time_and_date,
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingEditForm(data=form_data, instance=booking)
        self.assertTrue(form.is_valid())


    def test_booking_edit_with_invalid_data(self):
        booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber,
            date_and_hour=self.valid_time_and_date
        )

        form_data = {
            'date_and_hour': self.formated_now_with_invalid_hour, #The hour is invalid
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        form = BookingEditForm(data=form_data, instance=booking)
        self.assertFalse(form.is_valid())
        self.assertIn('date_and_hour', form.errors)
        self.assertEqual(
            form.errors['date_and_hour'][0],
            'Please select a valid time slot (e.g. 10:00 or 10:30).'
        )