from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.permissions import HasFullAccessPermission
from api.serializers.bookings import BookingSerializer
from bookings.models import Booking


class ListCreateBookingView(ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.has_perm('accounts.have_full_access'):
            return Booking.objects.select_related('barber').prefetch_related('services__bookings')
        return (Booking.objects.filter
                (user_profile=self.request.user.user_profile)
                .select_related('barber').prefetch_related('services__bookings'))

    def get_permissions(self):
        return [IsAuthenticated()]



class RetrieveUpdateDestroyBookingView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer


    def get_queryset(self):
        if self.request.user.has_perm('accounts.have_full_access'):
            return Booking.objects.select_related('barber').prefetch_related('services__bookings')
        return (Booking.objects.filter
                (user_profile=self.request.user.user_profile)
                .select_related('barber').prefetch_related('services__bookings'))

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [HasFullAccessPermission()]

        elif self.request.method == 'GET':
            return [IsAuthenticated()]

        else:
            return [AllowAny()]