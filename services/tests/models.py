import os
import django
from django.test import TestCase

from services.models import Service, Barber

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber_shop.settings')
django.setup()


class ServiceTest(TestCase):
    def setUp(self):
        self.test_service = Service.objects.create(
            name='Test',
            price=10,
            duration=30,
            description='Test Test',
            image_url='https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg'
        )

    def test_service_slug_creates_correctly(self):
        expected_slug = 'test'
        self.assertEqual(self.test_service.slug, expected_slug)


    def test_slug_does_not_change_on_update(self):
        original_slug = self.test_service.slug
        self.test_service.name = 'New Name'
        self.test_service.save()
        self.test_service.refresh_from_db()
        self.assertEqual(self.test_service.slug, original_slug)


    def test_slug_handles_special_characters(self):
        service_with_special_characters = Service.objects.create(
            name='Best!!!?>.',
            price=10,
            duration=30,
            description='Test tintiri mintiri Test',
            image_url='https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg'
        )

        expected_slug = 'best'
        self.assertEqual(service_with_special_characters.slug, expected_slug)

    def test_str_method_works_correctly(self):
        expected_output = 'Test (10 euro)'
        self.assertEqual(str(self.test_service), expected_output)

    def test_str_method_changes_when_price_and_name_change(self):
        self.test_service.price = 15
        self.test_service.name = 'Changed'
        expected_output = 'Changed (15 euro)'
        self.assertEqual(str(self.test_service), expected_output)



class BarberTest(TestCase):
    def setUp(self):
        self.test_barber = Barber.objects.create(
            first_name='Test',
            last_name='Barber',
            image_url='https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
            bio='Lorem Ipson...',
            years_of_experience=4,
        )

    def test_barber_slug_creates_correctly(self):
        expected_slug = 'test-barber'
        self.assertEqual(self.test_barber.slug, expected_slug)


    def test_barber_does_not_change_on_update(self):
        original_slug = self.test_barber.slug
        self.test_barber.first_name = 'New'
        self.test_barber.save()
        self.test_barber.refresh_from_db()
        self.assertEqual(self.test_barber.slug, original_slug)


    def test_slug_handles_special_characters(self):
        barber_with_special_characters = Barber.objects.create(
            first_name='New!!!@>?,.',
            last_name='Barber',
            image_url='https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
            bio='Lorem Ipson...',
            years_of_experience=4,
        )

        expected_slug = 'new-barber'
        self.assertEqual(barber_with_special_characters.slug, expected_slug)

    def test_str_method_works_correctly(self):
        expected_output = 'Test Barber'
        self.assertEqual(str(self.test_barber), expected_output)

    def test_str_method_changes_when_name_change(self):
        self.test_barber.first_name = 'Changed'
        self.test_barber.last_name = 'New'
        expected_output = 'Changed New'
        self.assertEqual(str(self.test_barber), expected_output)