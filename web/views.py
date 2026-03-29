from django.db.models.aggregates import Count
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from django.shortcuts import render

from reviews.models import Review
from services.models import Barber


def index(request: HttpRequest) -> HttpResponse:
    top_three_barbers = Barber.objects.annotate(bookings_count=Count('bookings')).order_by('-bookings_count')[:3]
    last_five_reviews = Review.objects.all().order_by('-created_at')[:5]
    context = {
        'top_three_barbers': top_three_barbers,
        'last_five_reviews': last_five_reviews
    }
    return render(request, 'web/home-page.html', context)


