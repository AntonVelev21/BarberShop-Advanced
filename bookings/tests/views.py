from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from bookings.models import Booking
from services.models import Service, Barber


class BookingTestBase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='worker1',
            password='test1234'
        )

        self.admin_user = User.objects.create_user(
            username='boss',
            password='test1234'
        )

        permission = Permission.objects.get(codename='have_full_access')
        self.admin_user.user_permissions.add(permission)

        self.barber = Barber.objects.create(
            first_name='test3',
            last_name='test',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s',
            bio='Test',
            years_of_experience=4,

        )

        self.service1 = Service.objects.create(
            name='Test1',
            price=5,
            duration=50,
            description='Test',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s'
        )

        self.service2 = Service.objects.create(
            name='Test2',
            price=56,
            duration=50,
            description='Test',
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxOFvr7KdOLpK-eBEQC4MZ5w9bP88Nppxklw&s'
        )

        self.booking = Booking.objects.create(
            user_profile=self.user1.user_profile,
            barber=self.barber,
            date_and_hour='3026-04-14 14:30'
        )


class BookingAccessControlTest(BookingTestBase):
    def test_list_view_status_code(self):
        self.client.login(username='worker1', password='test1234')
        response = self.client.get(reverse('bookings:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/list.html')


    def test_anonymous_user_login_redirect(self):
        urls = [
            reverse('bookings:create'),
            reverse('bookings:edit', kwargs={'pk': self.booking.pk}),
            reverse('bookings:delete', kwargs={'pk': self.booking.pk})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)


    def test_user_has_no_permission_forbidden(self):
        self.client.login(username='worker1', password='test1234')
        urls = [
            reverse('bookings:edit', kwargs={'pk': self.booking.pk}),
            reverse('bookings:delete', kwargs={'pk': self.booking.pk})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)



class BookingCRUDTest(BookingTestBase):
    def setUp(self):
        super().setUp()


    def test_create_booking_form_authenticated_basic_user_success(self):
        self.client.login(username='worker1', password='test1234')
        data = {
            'user_profile': self.user1.user_profile.pk,
            'barber': self.barber.pk,
            'date_and_hour': '3026-04-14 15:30',
            'services': [self.service1.pk, self.service2.pk]
        }

        response = self.client.post(reverse('bookings:create'), data)
        self.assertRedirects(response, reverse('home-page'))
        self.assertTrue(Booking.objects.filter(user_profile=self.user1.user_profile,
                                               barber=self.barber,
                                               date_and_hour='3026-04-14 15:30').exists())


    def test_edit_booking_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('bookings:edit', kwargs={'pk': self.booking.pk})
        data = {
            'user_profile': self.user1.user_profile.pk,
            'barber': self.barber.pk,
            'date_and_hour': '3026-04-14 16:30',
            'services': [self.service1.pk, self.service2.pk]
        }

        response = self.client.post(url, data)
        self.booking.refresh_from_db()
        self.assertEqual(
            self.booking.date_and_hour.strftime("%Y-%m-%d %H:%M"),
            '3026-04-14 16:30'
        )


    def test_delete_booking_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('bookings:delete', kwargs={'pk': self.booking.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home-page'))
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())








