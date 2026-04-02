from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy

from accounts.models import UserProfile
from services.forms import BarberCreateForm, ServiceCreateForm, BarberEditForm, ServiceEditForm
from services.models import Barber, Service



class ListBarbersView(ListView):
    model = Barber
    context_object_name = 'barbers'
    template_name = 'barbers/list.html'



class DetailsBarberView(DetailView):
    model = Barber
    context_object_name = 'barber'
    template_name = 'barbers/details.html'



class CreateBarberView(LoginRequiredMixin, CreateView):
    model = Barber
    form_class = BarberCreateForm
    template_name = 'barbers/form.html'
    success_url = reverse_lazy('home-page')

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)



class EditBarberView(LoginRequiredMixin, UpdateView):
    model = Barber
    form_class = BarberEditForm
    template_name = 'barbers/form.html'
    success_url = reverse_lazy('home-page')

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)



class DeleteBarberView(LoginRequiredMixin, DeleteView):
    model = Barber
    template_name = 'barbers/delete.html'
    success_url = reverse_lazy('home-page')

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)



class ListServicesView(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'services/list.html'



class DetailsServicesView(DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'services/details.html'



class CreateServiceView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceCreateForm
    template_name = 'services/form.html'
    success_url = reverse_lazy('home-page')

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)



class EditServiceView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceEditForm
    template_name = 'services/form.html'
    success_url = reverse_lazy('home-page')

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)



class DeleteServiceView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'services/delete.html'
    success_url = reverse_lazy('home-page')

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)