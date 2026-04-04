from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from api.serializers.bookings import BookingSerializer
from bookings.models import Booking


class ListCreateBookingView(LoginRequiredMixin, ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.has_perm('accounts.have_full_access'):
            return Booking.objects.select_related('barber').prefetch_related('services__bookings')
        return (Booking.objects.filter
                (user_profile=self.request.user.user_profile)
                .select_related('barber').prefetch_related('services__bookings'))



class RetrieveUpdateDestroyBookingView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.has_perm('accounts.have_full_access'):
            return Booking.objects.select_related('barber').prefetch_related('services__bookings')
        return (Booking.objects.filter
                (user_profile=self.request.user.user_profile)
                .select_related('barber').prefetch_related('services__bookings'))