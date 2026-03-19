from django.urls.conf import path, include

from services.views import ListBarbersView, DetailsBarberView, CreateBarberView, EditBarberView, DeleteBarberView, ListServicesView, \
    DetailsServicesView, CreateServiceView, EditServiceView, DeleteServiceView

app_name = 'services'


barbers_patterns = [
    path('', ListBarbersView.as_view(), name='list-barbers'),
    path('create/', CreateBarberView.as_view(), name='create-barber'),
    path('<slug:slug>/', include([
        path('', DetailsBarberView.as_view(), name='barber-details'),
        path('edit/', EditBarberView.as_view(), name='edit-barber'),
        path('delete/', DeleteBarberView.as_view(), name='delete-barber')
    ]))
]

services_patterns = [
    path('', ListServicesView.as_view(), name='list-services'),
    path('create/', CreateServiceView.as_view(), name='create-service'),
    path('<slug:slug>/', include([
        path('', DetailsServicesView.as_view(), name='service-details'),
        path('edit/', EditServiceView.as_view(), name='edit-service'),
        path('delete/', DeleteServiceView.as_view(), name='delete-service')
    ]))

]

urlpatterns = [
    path('barbers/', include(barbers_patterns)),
    path('', include(services_patterns))
]