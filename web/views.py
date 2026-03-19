from django.db.models.aggregates import Count
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from django.shortcuts import render
from services.models import Barber


def index(request: HttpRequest) -> HttpResponse:
    top_three_barbers = Barber.objects.annotate(bookings_count=Count('bookings')).order_by('-bookings_count')[:3]
    context = {
        'top_three_barbers': top_three_barbers
    }
    return render(request, 'web/home-page.html', context)


