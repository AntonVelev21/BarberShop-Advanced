from django.urls.conf import path, include

from services.views import list_services, create_service, service_details, edit_service, delete_service, list_barbers, \
    barber_details, edit_barber, delete_barber, create_barber

app_name = 'services'


barbers_patterns = [
    path('', list_barbers, name='list-barbers'),
    path('create/', create_barber, name='create-barber'),
    path('<slug:slug>/', include([
        path('', barber_details, name='barber-details'),
        path('edit/', edit_barber, name='edit-barber'),
        path('delete/', delete_barber, name='delete-barber')
    ]))
]

services_patterns = [
    path('', list_services, name='list-services'),
    path('create/', create_service, name='create-service'),
    path('<slug:slug>/', include([
        path('', service_details, name='service-details'),
        path('edit/', edit_service, name='edit-service'),
        path('delete/', delete_service, name='delete-service')
    ]))

]

urlpatterns = [
    path('barbers/', include(barbers_patterns)),
    path('', include(services_patterns))
]