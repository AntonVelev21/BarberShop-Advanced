from django.urls import path, include

from api.views.barbers import ListCreateBarberView, RetrieveUpdateDestroyBarberView
from api.views.bookings import ListCreateBookingView
from api.views.reviews import ListCreateReviewView, RetrieveUpdateDestroyReviewView
from api.views.services import ListCreateServiceView, RetrieveUpdateDestroyServiceView

app_name = 'api'


barbers_patterns = [
    path('', ListCreateBarberView.as_view(), name='barber-list'),
    path('<int:pk>/', RetrieveUpdateDestroyBarberView.as_view(), name='barber-detail')

]

services_patterns = [
    path('', ListCreateServiceView.as_view(), name='services-list'),
    path('<int:pk>/', RetrieveUpdateDestroyServiceView.as_view(), name='service-detail')
]


reviews_pattern = [
    path('', ListCreateReviewView.as_view(), name='reviews-list'),
    path('<int:pk>/', RetrieveUpdateDestroyReviewView.as_view(), name='review-detail')
]


bookings_pattern = [
    path('', ListCreateBookingView.as_view(), name='bookings-list'),
]


urlpatterns = [
    path('barbers/', include(barbers_patterns)),
    path('services/', include(services_patterns)),
    path('reviews/', include(reviews_pattern)),
    path('bookings/', include(bookings_pattern))
]

