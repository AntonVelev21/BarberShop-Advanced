from django.urls import reverse

from reviews.models import Review
from reviews.tests.views import ReviewTestBase
from rest_framework.test import APITestCase


class TestListCreateReviewAPIView(ReviewTestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'title': 'Test',
            'content': 'Lorem Ipson',
            'rating': 4,
            'barber': {
                'first_name': 'Test2',
                'last_name': 'Example2',
                'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
                'bio': 'Lorem Ipson...',
                'years_of_experience': 5
            }
        }


    def test_list_reviews_status_code(self):
        response = self.client.get(reverse('api:review-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Lorem Ipson')


    def test_review_create_without_authentication_expect_expect_forbidden(self):
        response = self.client.post(reverse('api:review-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, 403)


    def test_review_create_when_authenticated_but_does_not_have_permission_expect_success(self):
        self.client.login(username='worker', password='test1234')
        response = self.client.post(reverse('api:review-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_review_create_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        response = self.client.post(reverse('api:review-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, 201)





class TestRetrieveUpdateDestroyReviewAPIView(ReviewTestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.put_data = {
            'title': 'Edited review',
            'content': 'Lorem Ipson Updated',
            'rating': 4,
            'barber': {
                'first_name': 'Test2',
                'last_name': 'Example2',
                'image_url': 'https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg',
                'bio': 'Lorem Ipson...',
                'years_of_experience': 4
            }
        }

        self.patch_data = {
            'title': 'Patched Test'
        }


    def test_review_details_status_code(self):
        response = self.client.get(reverse('api:review-detail', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], 'Lorem Ipson')



    def test_review_edit_without_authentication_expect_expect_forbidden(self):
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        response = self.client.put(url, data=self.put_data, format='json')
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 403)



    def test_review_edit_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        response = self.client.put(url, data=self.put_data, format='json')
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 403)



    def test_review_edit_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        response = self.client.put(url, data=self.put_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Edited review')

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 200)
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Patched Test')



    def test_review_delete_without_authentication_expect_expect_forbidden(self):
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



    def test_review_delete_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



    def test_review_delete_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('api:review-detail', kwargs={'pk': self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())