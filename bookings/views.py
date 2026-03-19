from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from bookings.forms import BookingCreateForm, BookingDeleteForm, BookingEditForm
from bookings.models import Booking
from services.models import Barber



class ListBookingsView(ListView):
    model = Booking
    context_object_name = 'bookings'
    template_name = 'bookings/list.html'



class CreateBookingView(CreateView):
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



class EditBookingView(UpdateView):
    form_class = BookingEditForm
    model = Booking
    template_name = 'bookings/form.html'
    success_url = reverse_lazy('home-page')



class DeleteBookingView(DeleteView):
    model = Booking
    template_name = 'bookings/delete.html'
    success_url = reverse_lazy('home-page')

