from django.test import TestCase
from api.serializers.barbers import BarberSerializer
from services.models import Barber


class BarberSerializerTests(TestCase):
    def setUp(self):
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

        self.barber_data_with_missing_field = {
            'first_name': 'Test',
            'last_name': 'Example',
            'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
            'bio': 'Lorem Ipson...',
                                        # years_of_experience is missing
        }

        self.barber = Barber.objects.create(
            first_name='Test',
            last_name='Example',
            image_url='https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
            bio='Lorem Ipson...',
            years_of_experience=4
        )


    def test_serializer_with_valid_data_and_excludes_slug(self):
        serializer = BarberSerializer(data=self.valid_barber_data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('slug', serializer.data)


    def test_serializer_with_invalid_data(self):
        serializer = BarberSerializer(data=self.invalid_barber_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('years_of_experience', serializer.errors)


    def test_serializer_with_missing_data(self):
        serializer = BarberSerializer(data=self.barber_data_with_missing_field)
        self.assertFalse(serializer.is_valid())
        self.assertIn('years_of_experience', serializer.errors)
        self.assertEqual(serializer.errors['years_of_experience'][0], 'This field is required.')


    def test_barber_edit_with_valid_data(self):
        serializer = BarberSerializer(data=self.valid_barber_data, instance=self.barber)
        self.assertTrue(serializer.is_valid())


    def test_barber_edit_with_invalid(self):
        serializer = BarberSerializer(data=self.invalid_barber_data, instance=self.barber)
        self.assertFalse(serializer.is_valid())
        self.assertIn('years_of_experience', serializer.errors)