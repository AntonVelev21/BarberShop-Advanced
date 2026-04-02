from django.urls import path, include

from api.views.barbers import ListCreateBarber, RetrieveUpdateDestroyBarberView

app_name = 'api'

urlpatterns = [
    path('barbers/', include([
        path('', ListCreateBarber.as_view(), name='barber-list'),
        path('<int:pk>/', RetrieveUpdateDestroyBarberView.as_view(), name='barber-detail')
    ]))
]

