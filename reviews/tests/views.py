from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from reviews.models import Review
from services.models import Barber


class ReviewTestBase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='worker',
            password='test1234'
        )

        self.admin_user = User.objects.create_user(
            username='boss',
            password='test1234'
        )

        permission = Permission.objects.get(codename='have_full_access')
        self.admin_user.user_permissions.add(permission)

        self.barber = Barber.objects.create(
            first_name='test',
            last_name='example',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            bio='Test',
            years_of_experience=4,
        )

        self.review = Review.objects.create(
            title='Test',
            author=self.user.user_profile,
            content='Lorem Ipson',
            rating=5,
            barber=self.barber,
        )


class ReviewPublicViewsTests(ReviewTestBase):
    def test_list_view_status_code(self):
        response = self.client.get(reverse('reviews:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/list.html')


    def test_detail_view_status_code(self):
        response = self.client.get(reverse('reviews:details', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['review'], self.review)




class ReviewAccessControlTest(ReviewTestBase):
    def test_anonymous_user_login_redirect(self):
        urls = [
            reverse('reviews:create'),
            reverse('reviews:edit', kwargs={'pk': self.review.pk}),
            reverse('reviews:delete', kwargs={'pk': self.review.pk})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)


    def test_user_has_no_permission_forbidden(self):
        self.client.login(username='worker', password='test1234')
        urls = [
            reverse('reviews:edit', kwargs={'pk': self.review.pk}),
            reverse('reviews:delete', kwargs={'pk': self.review.pk})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)




class ReviewCRUDTest(ReviewTestBase):
    def setUp(self):
        super().setUp()


    def test_create_review_form_authenticated_basic_user_success(self):
        self.client.login(username='worker', password='test1234')
        data = {
            'title': 'Test form worker',
            'author': self.user.user_profile.pk,
            'content': 'Lorem Ipson',
            'rating': 4,
            'barber': self.barber.pk
        }

        response = self.client.post(reverse('reviews:create'), data)
        self.assertRedirects(response, reverse('home-page'))
        self.assertTrue(Review.objects.filter(title='Test form worker').exists())


    def test_edit_booking_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('reviews:edit', kwargs={'pk': self.review.pk})
        data = {
            'title': 'Updated***',
            'author': self.user.user_profile.pk,
            'content': 'Lorem Ipson',
            'rating': 4,
            'barber': self.barber.pk
        }
        response = self.client.post(url, data)
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Updated***')


    def test_delete_booking_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('reviews:delete', kwargs={'pk': self.review.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home-page'))
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())