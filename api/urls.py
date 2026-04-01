from django.urls import path

from api.views.barbers import ListCreateBarber

app_name = 'api'

urlpatterns = [
    path('barbers/', ListCreateBarber.as_view(), name='list_create_barber')
]