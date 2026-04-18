from django.urls import reverse
from rest_framework.test import APITestCase

from services.models import Barber
from services.tests.barber_views import BarberTestBase


class TestListCreateBarberAPIView(BarberTestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'first_name': 'New',
            'last_name': 'Barber',
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            'bio': 'Some random text',
            'years_of_experience': 5
        }


    def test_list_barbers_status_code(self):
        response = self.client.get(reverse('api:barber-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'test')


    def test_barber_create_without_authentication_expect_expect_forbidden(self):
        response = self.client.post(reverse('api:barber-list'), data=self.data)
        self.assertEqual(response.status_code, 403)


    def test_barber_create_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        response = self.client.post(reverse('api:barber-list'), data=self.data)
        self.assertEqual(response.status_code, 403)


    def test_barber_create_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        response = self.client.post(reverse('api:barber-list'), data=self.data)
        self.assertEqual(response.status_code, 201)




class TestRetrieveUpdateDestroyBarberAPIView(BarberTestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.put_data = {
            'first_name': 'New Updated',
            'last_name': 'Barber',
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            'bio': 'Some random text',
            'years_of_experience': 5
        }
        self.patch_data = {
            'last_name': 'Barber Updated'
        }


    def test_barber_details_status_code(self):
        response = self.client.get(reverse('api:barber-detail', kwargs={'pk': self.barber.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'test')



    def test_barber_edit_without_authentication_expect_expect_forbidden(self):
        url = reverse('api:barber-detail', kwargs={'pk': self.barber.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 403)



    def test_barber_edit_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        url = reverse('api:barber-detail', kwargs={'pk': self.barber.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 403)



    def test_barber_edit_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('api:barber-detail', kwargs={'pk': self.barber.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 200)
        self.barber.refresh_from_db()
        self.assertEqual(self.barber.first_name, 'New Updated')

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 200)
        self.barber.refresh_from_db()
        self.assertEqual(self.barber.last_name, 'Barber Updated')



    def test_barber_delete_without_authentication_expect_expect_forbidden(self):
        url = reverse('api:barber-detail', kwargs={'pk': self.barber.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



    def test_barber_delete_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        url = reverse('api:barber-detail', kwargs={'pk': self.barber.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



    def test_barber_delete_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('api:barber-detail', kwargs={'pk': self.barber.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Barber.objects.filter(pk=self.barber.pk).exists())



