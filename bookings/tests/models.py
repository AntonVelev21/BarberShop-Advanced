import os
import django
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber_shop.settings')
django.setup()

from django.contrib.auth.models import User
from bookings.models import Booking
from services.models import Barber, Service


class BookingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_userrr',
            password='test1234'
        )

        self.barber = Barber.objects.create(
            first_name='test1',
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

        self.test_booking = Booking.objects.create(
            user_profile=self.user.user_profile,
            barber=self.barber
        )

        self.test_booking.services.set([self.service1, self.service2])

    def test_booking_total_price_is_correct(self):
        self.assertEqual(self.test_booking.total_price, 61)

    def test_booking_total_price_is_not_correct(self):
        self.assertNotEqual(self.test_booking.total_price, 62)

    def test_booking_total_price_updates_on_additional_service(self):
        old_price = self.test_booking.total_price
        extra_service = Service.objects.create(
            name='additional',
            price=10,
            duration=50,
            description='Test',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s'
        )
        self.test_booking.services.add(extra_service)

        self.assertEqual(self.test_booking.total_price, 71)
        self.assertNotEqual(self.test_booking.total_price, old_price)
