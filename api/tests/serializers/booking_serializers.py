from django.contrib.auth.models import User
from django.test import TestCase

from api.serializers.bookings import BookingSerializer
from bookings.models import Booking
from services.models import Barber, Service


class BookingSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
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


        self.booking_valid_data = {
            'date_and_hour': '3026-04-15 14:30',
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }


        self.booking_invalid_time_slot = {
            'date_and_hour': '3026-04-15 14:35',
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }


        self.booking_hour_outside_of_working_hours = {
            'date_and_hour': '3026-04-15 21:30',
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        self.booking_day_is_rest_day= {
            'date_and_hour': '3026-04-16 21:30',  #Sunday
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }

        self.booking_date_and_hour_is_in_the_past = {
            'date_and_hour': '2026-04-15 21:30',
            'barber': self.barber.id,
            'services': [self.service1.id, self.service2.id]
        }


    def test_booking_create_with_valid_data(self):
        serializer = BookingSerializer(data=self.booking_valid_data)
        self.assertTrue(serializer.is_valid())


    def test_booking_create_with_invalid_time_slot(self):
        serializer = BookingSerializer(data=self.booking_invalid_time_slot)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_and_hour', serializer.errors)
        self.assertEqual(
            serializer.errors['date_and_hour'][0],
            'Please select a valid time slot (e.g. 10:00 or 10:30).'
        )


    def test_booking_create_with_hour_outside_of_working_hours(self):
        serializer = BookingSerializer(data=self.booking_hour_outside_of_working_hours)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_and_hour', serializer.errors)
        self.assertEqual(
            serializer.errors['date_and_hour'][0],
            'Our working hours are between 09:00 and 18:00.'
        )


    def test_booking_create_with_rest_day(self):
        serializer = BookingSerializer(data=self.booking_day_is_rest_day)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_and_hour', serializer.errors)
        self.assertEqual(
            serializer.errors['date_and_hour'][0],
            'Please choose a working day. We work from Monday to Saturday.'
        )


    def test_booking_create_with_date_and_hour_in_the_past(self):
        serializer = BookingSerializer(data=self.booking_date_and_hour_is_in_the_past)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_and_hour', serializer.errors)
        self.assertEqual(
            serializer.errors['date_and_hour'][0],
            'You cannot book a seat in the past!'
        )

    def test_serializer_with_existing_booking(self):
        booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber,
            date_and_hour=self.booking_valid_data['date_and_hour']
        )

        serializer = BookingSerializer(data=self.booking_valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_and_hour', serializer.errors)
        self.assertEqual(
            serializer.errors['date_and_hour'][0],
            'Sorry, test3 is already booked for this time. Please choose another.'
        )


    def test_booking_edit_with_the_same_time_is_valid(self):
        booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber,
            date_and_hour=self.booking_valid_data['date_and_hour']
        )

        serializer = BookingSerializer(data=self.booking_valid_data, instance=booking)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())


    def test_booking_edit_with_invalid_data(self):
        booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber,
            date_and_hour=self.booking_valid_data['date_and_hour']
        )

        serializer = BookingSerializer(data=self.booking_invalid_time_slot, instance=booking)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_and_hour', serializer.errors)
        self.assertEqual(
            serializer.errors['date_and_hour'][0],
            'Please select a valid time slot (e.g. 10:00 or 10:30).'
        )


