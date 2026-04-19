from django.urls import reverse

from services.models import Service
from services.tests.service_views import ServiceTestBase
from rest_framework.test import APITestCase


class TestListCreateServiceAPIView(ServiceTestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'name': 'New service',
            'price': 5,
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            'description': 'Some random text',
            'duration': 5
        }


    def test_list_services_status_code(self):
        response = self.client.get(reverse('api:service-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test service')


    def test_service_create_without_authentication_expect_expect_forbidden(self):
        response = self.client.post(reverse('api:service-list'), data=self.data)
        self.assertEqual(response.status_code, 403)


    def test_service_create_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        response = self.client.post(reverse('api:service-list'), data=self.data)
        self.assertEqual(response.status_code, 403)


    def test_service_create_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        response = self.client.post(reverse('api:service-list'), data=self.data)
        self.assertEqual(response.status_code, 201)




class TestRetrieveUpdateDestroyServiceAPIView(ServiceTestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.put_data = {
            'name': 'Edited service',
            'price': 5,
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            'description': 'Some random text',
            'duration': 5
        }

        self.patch_data = {
            'description': 'Some random text patched'
        }

    def test_service_details_status_code(self):
        response = self.client.get(reverse('api:service-detail', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test service')



    def test_service_edit_without_authentication_expect_expect_forbidden(self):
        url = reverse('api:service-detail', kwargs={'pk': self.service.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 403)



    def test_service_edit_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        url = reverse('api:service-detail', kwargs={'pk': self.service.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 403)



    def test_service_edit_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('api:service-detail', kwargs={'pk': self.service.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 200)
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Edited service')

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 200)
        self.service.refresh_from_db()
        self.assertEqual(self.service.description, 'Some random text patched')



    def test_service_delete_without_authentication_expect_expect_forbidden(self):
        url = reverse('api:service-detail', kwargs={'pk': self.service.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



    def test_service_delete_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        url = reverse('api:service-detail', kwargs={'pk': self.service.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



    def test_service_delete_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('api:service-detail', kwargs={'pk': self.service.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Service.objects.filter(pk=self.service.pk).exists())