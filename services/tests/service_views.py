from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from services.models import Service


class ServiceTestBase(TestCase):
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

        self.service = Service.objects.create(
            name='Test service',
            price=20,
            duration=40,
            description='Testing...',
            image_url='https://www.k12digest.com/wp-content/uploads/2024/03/1-3-550x330.jpg'
        )


class ServicePublicViewsTests(ServiceTestBase):
    def test_list_view_status_code(self):
        response = self.client.get(reverse('services:list-services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/list.html')


    def test_detail_view_status_code(self):
        response = self.client.get(reverse('services:service-details', kwargs={'slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['service'], self.service)



class ServiceAccessControlTest(ServiceTestBase):
    def test_anonymous_user_login_redirect(self):
        urls = [
            reverse('services:create-service'),
            reverse('services:edit-service', kwargs={'slug': self.service.slug}),
            reverse('services:delete-service', kwargs={'slug': self.service.slug})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)


    def test_user_has_no_permission_forbidden(self):
        self.client.login(username='worker', password='test1234')
        urls = [
            reverse('services:create-service'),
            reverse('services:edit-service', kwargs={'slug': self.service.slug}),
            reverse('services:delete-service', kwargs={'slug': self.service.slug})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)



class ServiceCRUDTest(ServiceTestBase):
    def setUp(self):
        super().setUp()
        self.client.login(username='boss', password='test1234')


    def test_create_service_success(self):
        data = {
            'name': 'New service',
            'price': 5,
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            'description': 'Some random text',
            'duration': 5
        }

        response = self.client.post(reverse('services:create-service'), data)
        self.assertRedirects(response, reverse('home-page'))
        self.assertTrue(Service.objects.filter(name='New service').exists())


    def test_edit_service_success(self):
        url = reverse('services:edit-service', kwargs={'slug': self.service.slug})
        data = {
            'name': 'Edited service',
            'price': 5,
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            'description': 'Some random text',
            'duration': 5
        }
        response = self.client.post(url, data)
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Edited service')


    def test_delete_service_success(self):
        url = reverse('services:delete-service', kwargs={'slug': self.service.slug})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home-page'))
        self.assertFalse(Service.objects.filter(id=self.service.id).exists())