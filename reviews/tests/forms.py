from django.contrib.auth.models import User
from django.test import TestCase

from reviews.forms import ReviewCreateForm, ReviewEditForm
from reviews.models import Review
from services.models import Barber



class ReviewFormTests(TestCase):
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
            'barber': self.barber
        }

        self.invalid_review_data_with_less_then_minimum_rating = {
            'title': 'Test',
            'author': self.author.user_profile,
            'content': 'Lorem Ipson',
            'rating': -2,
            'barber': self.barber
        }

        self.invalid_review_data_with_more_then_maximum_rating = {
            'title': 'Test',
            'author': self.author.user_profile,
            'content': 'Lorem Ipson',
            'rating': 7,
            'barber': self.barber
        }

    def test_review_create_with_valid_data(self):
        form = ReviewCreateForm(data=self.valid_review_data)
        self.assertTrue(form.is_valid())


    def test_review_create_with_less_then_minimum_rating(self):
        form = ReviewCreateForm(data=self.invalid_review_data_with_less_then_minimum_rating)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertEqual(
            form.errors['rating'][0],
            'You can not put negative rating!'
        )


    def test_review_create_with_more_then_maximum_rating(self):
        form = ReviewCreateForm(data=self.invalid_review_data_with_more_then_maximum_rating)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertEqual(
            form.errors['rating'][0],
            '5 is the maximum rating.'
        )


    def test_review_create_with_missing_data(self):
        form_data = {
                                                     #Title is missing
             'author': self.author.user_profile,
            'content': 'Lorem Ipson',
            'rating': 7,
            'barber': self.barber
        }

        form = ReviewCreateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(
            form.errors['title'][0],
            'This field is required.'
        )


    def test_review_edit_with_valid_data(self):
        form = ReviewEditForm(data=self.valid_review_data, instance=self.review)
        self.assertTrue(form.is_valid())


    def test_review_edit_with_invalid_data(self):
        form = ReviewEditForm(data=self.invalid_review_data_with_less_then_minimum_rating, instance=self.review)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertEqual(
            form.errors['rating'][0],
            'You can not put negative rating!'
        )