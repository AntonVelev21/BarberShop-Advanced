from time import strftime

from django.urls import reverse

from bookings.models import Booking
from bookings.tests.views import BookingTestBase
from rest_framework.test import APITestCase



class TestListCreateBookingAPIView(BookingTestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'user_profile': self.user1.user_profile.pk,
            'barber': self.barber.pk,
            'date_and_hour': '3026-04-14 15:30',
            'services': [self.service1.pk, self.service2.pk]
        }


    def test_list_bookings_without_authentication_status_code_expect_forbidden(self):
        response = self.client.get(reverse('api:booking-list'))
        self.assertEqual(response.status_code, 403)


    def test_list_bookings_expect_success(self):
        self.client.login(username='worker1', password='test1234')
        response = self.client.get(reverse('api:booking-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.booking.id)


    def test_booking_create_without_authentication_expect_expect_forbidden(self):
        response = self.client.post(reverse('api:booking-list'), data=self.data)
        self.assertEqual(response.status_code, 403 )


    def test_booking_create_when_authenticated_but_does_not_have_permission_expect_success(self):
        self.client.login(username='worker1', password='test1234')
        response = self.client.post(reverse('api:booking-list'), data=self.data)
        self.assertEqual(response.status_code, 201)


    def test_booking_create_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        response = self.client.post(reverse('api:booking-list'), data=self.data)
        self.assertEqual(response.status_code, 201)




class TestRetrieveUpdateDestroyBookingAPIView(BookingTestBase, APITestCase):
    def setUp(self):
        super().setUp()
        self.put_data = {
            'user_profile': self.user1.user_profile.pk,
            'barber': self.barber.pk,
            'date_and_hour': '3026-04-14 17:30',
            'services': [self.service1.pk]
        }

        self.patch_data = {
            'date_and_hour': '3026-04-14 18:30'
        }


    def test_booking_details_without_authentication_status_code_expect_forbidden(self):
        response = self.client.get(reverse('api:booking-detail', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 403)


    def test_booking_details_expect_success(self):
        self.client.login(username='worker1', password='test1234')
        response = self.client.get(reverse('api:booking-detail', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['date_and_hour'], '3026-04-14T14:30:00Z')


    def test_booking_edit_without_authentication_expect_expect_forbidden(self):
        url = reverse('api:booking-detail', kwargs={'pk': self.booking.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 403)



    def test_booking_edit_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        url = reverse('api:booking-detail', kwargs={'pk': self.booking.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 403)


#To do: Fix the barber patch issue!!!
#Finish the delete tests
#Look at the project for changes or upgrade
#Prepare project for deploy
#Deploy and send github url
    

    def test_booking_edit_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('api:booking-detail', kwargs={'pk': self.booking.pk})
        response = self.client.put(url, data=self.put_data)
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.date_and_hour.strftime("%Y-%m-%d %H:%M"), '3026-04-14 17:30')

        response = self.client.patch(url, data=self.patch_data)
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.date_and_hour.strftime("%Y-%m-%d %H:%M"), '3026-04-14 18:30')



    def test_booking_delete_without_authentication_expect_expect_forbidden(self):
        url = reverse('api:booking-detail', kwargs={'pk': self.booking.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



    def test_booking_delete_when_authenticated_but_does_not_have_permission_expect_forbidden(self):
        self.client.login(username='worker', password='test1234')
        url = reverse('api:booking-detail', kwargs={'pk': self.booking.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)



    def test_booking_delete_when_authenticated_and_authorized_expect_success(self):
        self.client.login(username='boss', password='test1234')
        url = reverse('api:booking-detail', kwargs={'pk': self.booking.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())