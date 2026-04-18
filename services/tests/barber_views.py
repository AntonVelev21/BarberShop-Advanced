from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from services.models import Barber


class BarberTestBase(TestCase):
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


class BarberPublicViewsTests(BarberTestBase):
    def test_list_view_status_code(self):
        response = self.client.get(reverse('services:list-barbers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'barbers/list.html')


    def test_detail_view_status_code(self):
        response = self.client.get(reverse('services:barber-details', kwargs={'slug': self.barber.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['barber'], self.barber)



class BarberAccessControlTest(BarberTestBase):
    def test_anonymous_user_login_redirect(self):
        urls = [
            reverse('services:create-barber'),
            reverse('services:edit-barber', kwargs={'slug': self.barber.slug}),
            reverse('services:delete-barber', kwargs={'slug': self.barber.slug})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)


    def test_user_has_no_permission_forbidden(self):
        self.client.login(username='worker', password='test1234')
        urls = [
            reverse('services:create-barber'),
            reverse('services:edit-barber', kwargs={'slug': self.barber.slug}),
            reverse('services:delete-barber', kwargs={'slug': self.barber.slug})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)



class BarberCRUDTest(BarberTestBase):
    def setUp(self):
        super().setUp()
        self.client.login(username='boss', password='test1234')


    def test_create_barber_success(self):
        data = {
            'first_name': 'New',
            'last_name': 'Barber',
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            'bio': 'Some random text',
            'years_of_experience': 5
        }

        response = self.client.post(reverse('services:create-barber'), data)
        self.assertRedirects(response, reverse('home-page'))
        self.assertTrue(Barber.objects.filter(first_name='New', last_name='Barber').exists())


    def test_edit_barber_success(self):
        url = reverse('services:edit-barber', kwargs={'slug': self.barber.slug})
        data = {
            'first_name': 'New test',
            'last_name': 'Edited Barber',
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            'bio': 'Some random text',
            'years_of_experience': 3
        }
        response = self.client.post(url, data)
        self.barber.refresh_from_db()
        self.assertEqual(self.barber.first_name, 'New test')


    def test_delete_barber_success(self):
        url = reverse('services:delete-barber', kwargs={'slug': self.barber.slug})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home-page'))
        self.assertFalse(Barber.objects.filter(id=self.barber.id))