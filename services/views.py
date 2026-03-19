from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from services.forms import BarberCreateForm, ServiceCreateForm, BarberDeleteForm, BarberEditForm, ServiceEditForm, \
    ServiceDeleteForm
from services.models import Barber, Service


def list_barbers(request: HttpRequest) -> HttpResponse:
    barbers = Barber.objects.all()
    context = {
        'barbers': barbers
    }
    return render(request, 'barbers/list.html', context)


def barber_details(request: HttpRequest, slug: str) -> HttpResponse:
    barber = get_object_or_404(Barber, slug=slug)
    context = {
        'barber': barber
    }
    return render(request, 'barbers/details.html', context)


def create_barber(request: HttpRequest) -> HttpResponse:
    form = BarberCreateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home-page')
    context = {
        'form': form
    }

    return render(request, 'barbers/form.html', context)



def edit_barber(request: HttpRequest, slug: str) -> HttpResponse:
    barber = get_object_or_404(Barber, slug=slug)
    form = BarberEditForm(request.POST or None, instance=barber)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home-page')
    context = {
        'form': form,
        'barber': barber
    }

    return render(request, 'barbers/form.html', context)


def delete_barber(request: HttpRequest, slug: str) -> HttpResponse:
    barber = get_object_or_404(Barber, slug=slug)
    form = BarberDeleteForm(request.POST or None, instance=barber)
    if request.method == 'POST':
        barber.delete()
        return redirect('home-page')
    context = {
        'form': form,
        'barber': barber
    }

    return render(request, 'barbers/delete.html', context)


def list_services(request: HttpRequest) -> HttpResponse:
    services = Service.objects.all()
    context = {
        'services': services
    }

    return render(request, 'services/list.html', context)


def service_details(request: HttpRequest, slug: str) -> HttpResponse:
    service = get_object_or_404(Service, slug=slug)
    context = {
        'service': service
    }
    return render(request, 'services/details.html', context)


def create_service(request: HttpRequest) -> HttpResponse:
    form = ServiceCreateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home-page')
    context = {
        'form': form
    }
    return render(request, 'services/form.html', context)


def edit_service(request: HttpRequest, slug: str) -> HttpResponse:
    service = get_object_or_404(Service, slug=slug)
    form = ServiceEditForm(request.POST or None, instance=service)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home-page')
    context = {
        'form': form,
        'service': service
    }
    return render(request, 'services/form.html', context)


def delete_service(request: HttpRequest, slug: str) -> HttpResponse:
    service = get_object_or_404(Service, slug=slug)
    form = ServiceDeleteForm(request.POST or None, instance=service)
    if request.method == 'POST':
        service.delete()
        return redirect('home-page')
    context = {
        'form': form,
        'service': service
    }

    return render(request, 'services/delete.html', context)