from django.urls import path, include

from api.views.barbers import ListCreateBarber, RetrieveUpdateDestroyBarberView
from api.views.services import ListCreateService, RetrieveUpdateDestroyServiceView

app_name = 'api'


barbers_patterns = [
    path('', ListCreateBarber.as_view(), name='barber-list'),
    path('<int:pk>/', RetrieveUpdateDestroyBarberView.as_view(), name='barber-detail')

]

services_patterns = [
    path('', ListCreateService.as_view(), name='services-list'),
    path('<int:pk>/', RetrieveUpdateDestroyServiceView.as_view(), name='service-detail')
]


urlpatterns = [
    path('barbers/', include(barbers_patterns)),
    path('services/', include(services_patterns)),
]

