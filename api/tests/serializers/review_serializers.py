from django.contrib.auth.models import User
from django.test import TestCase

from api.serializers.reviews import ReviewSerializer
from reviews.models import Review
from services.models import Barber


class ReviewSerializerTests(TestCase):
    def setUp(self):
        self.author = User.objects.create(
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

        self.review = Review.objects.create(
            title='Test',
            author=self.author.user_profile,
            content='Lorem Ipson',
            rating=5,
            barber=self.barber,
        )

        self.valid_review_data = {
            'title': 'Test',
            'author': self.author.user_profile,
            'content': 'Lorem Ipson',
            'rating': 4,
            'barber': {
                'first_name': 'Test',
                'last_name': 'Example',
                'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
                'bio': 'Lorem Ipson...',
                'years_of_experience': 5
            }
        }

        self.invalid_review_data= {
            'title': 'Test',
            'author': self.author.user_profile,
            'content': 'Lorem Ipson',
            'rating': -2,  #The rating is negative
            'barber': {
                'first_name': 'Test',
                'last_name': 'Example',
                'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
                'bio': 'Lorem Ipson...',
                'years_of_experience': 5
            }
        }

        self.review_data_with_missing_barber = {
            'title': 'Test',
            'author': self.author.user_profile,
            'content': 'Lorem Ipson',
            'rating': 3,
        }


    def test_serializer_with_valid_data(self):
        serializer = ReviewSerializer(data=self.valid_review_data)
        self.assertTrue(serializer.is_valid())


    def test_serializer_with_invalid_data(self):
        serializer = ReviewSerializer(data=self.invalid_review_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('rating', serializer.errors)


    def test_serializer_with_missing_data(self):
        serializer = ReviewSerializer(data=self.review_data_with_missing_barber)
        self.assertFalse(serializer.is_valid())
        self.assertIn('barber', serializer.errors)
        self.assertEqual(
            serializer.errors['barber'][0],
            'This field is required.'
        )


    def test_edit_review_with_valid_data(self):
        serializer = ReviewSerializer(data=self.valid_review_data, instance=self.review)
        self.assertTrue(serializer.is_valid())


    def test_edit_review_with_invalid_data(self):
        serializer = ReviewSerializer(data=self.invalid_review_data, instance=self.review)
        self.assertFalse(serializer.is_valid())
        self.assertIn('rating', serializer.errors)