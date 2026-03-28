from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from bookings.forms import BookingCreateForm, BookingEditForm
from bookings.models import Booking
from services.models import Barber



class ListBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    context_object_name = 'bookings'
    template_name = 'bookings/list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        user_profile = self.request.user.user_profile
        return Booking.objects.filter(user_profile=user_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=self.get_queryset(), **kwargs)
        context['history'] = self.get_queryset().filter(date_and_hour__lt=datetime.today())
        context['upcoming'] = self.get_queryset().filter(date_and_hour__gte=datetime.today())
        return context


class CreateBookingView(LoginRequiredMixin, CreateView):
    form_class = BookingCreateForm
    model = Booking
    template_name = 'bookings/form.html'
    success_url = reverse_lazy('home-page')
    def get_initial(self):
        initial = super().get_initial()
        barber_id = self.request.GET.get('barber')
        if barber_id:
            barber = get_object_or_404(Barber, id=barber_id)
            initial['barber'] = barber.id
        return initial

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user_profile = self.request.user.user_profile
        booking.save()
        return super().form_valid(form)



class EditBookingView(UpdateView):
    form_class = BookingEditForm
    model = Booking
    template_name = 'bookings/form.html'
    success_url = reverse_lazy('home-page')



class DeleteBookingView(DeleteView):
    model = Booking
    template_name = 'bookings/delete.html'
    success_url = reverse_lazy('home-page')

