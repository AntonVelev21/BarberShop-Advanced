from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy

from services.forms import BarberCreateForm, ServiceCreateForm, BarberDeleteForm, BarberEditForm, ServiceEditForm, \
    ServiceDeleteForm
from services.models import Barber, Service



class ListBarbersView(ListView):
    model = Barber
    context_object_name = 'barbers'
    template_name = 'barbers/list.html'



class DetailsBarberView(DetailView):
    model = Barber
    context_object_name = 'barber'
    template_name = 'barbers/details.html'



class CreateBarberView(CreateView):
    model = Barber
    form_class = BarberCreateForm
    template_name = 'barbers/form.html'
    success_url = reverse_lazy('home-page')



class EditBarberView(UpdateView):
    model = Barber
    form_class = BarberEditForm
    template_name = 'barbers/form.html'
    success_url = reverse_lazy('home-page')



class DeleteBarberView(DeleteView):
    model = Barber
    template_name = 'barbers/delete.html'
    success_url = reverse_lazy('home-page')



class ListServicesView(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'services/list.html'



class DetailsServicesView(DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'services/details.html'



class CreateServiceView(CreateView):
    model = Service
    form_class = ServiceCreateForm
    template_name = 'services/form.html'
    success_url = reverse_lazy('home-page')



class EditServiceView(UpdateView):
    model = Service
    form_class = ServiceEditForm
    template_name = 'services/form.html'
    success_url = reverse_lazy('home-page')



class DeleteServiceView(DeleteView):
    model = Service
    template_name = 'services/delete.html'
    success_url = reverse_lazy('home-page')