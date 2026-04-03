from django.urls import path, include

from api.views.barbers import ListCreateBarberView, RetrieveUpdateDestroyBarberView
from api.views.reviews import ListCreateReviewView
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
]

urlpatterns = [
    path('barbers/', include(barbers_patterns)),
    path('services/', include(services_patterns)),
    path('reviews/', include(reviews_pattern))
]

