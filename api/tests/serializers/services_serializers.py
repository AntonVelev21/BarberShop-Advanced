from django.test import TestCase

from api.serializers.services import ServiceSerializer
from services.models import Service


class ServiceSerializerTests(TestCase):
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

        self.service_data_with_missing_field = {
            'name': 'Test',
            # price is missing
            'duration': 40,
            'description': 'Testing...',
            'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg'
        }


    def test_serializer_with_valid_data_and_excludes_slug(self):
        serializer = ServiceSerializer(data=self.valid_service_data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('slug', serializer.data)


    def test_serializer_with_invalid_data(self):
        serializer = ServiceSerializer(data=self.invalid_service_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)


    def test_serializer_with_missing_data(self):
        serializer = ServiceSerializer(data=self.service_data_with_missing_field)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
        self.assertEqual(
            serializer.errors['price'][0],
            'This field is required.'
        )


    def test_service_edit_with_valid_data(self):
        serializer = ServiceSerializer(data=self.valid_service_data, instance=self.service)
        self.assertTrue(serializer.is_valid())


    def test_service_edit_with_invalid(self):
        serializer = ServiceSerializer(data=self.invalid_service_data, instance=self.service)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
