from django.urls.conf import path, include

from bookings.views import list_bookings, create_booking, edit_booking, delete_booking

app_name = 'bookings'

urlpatterns = [
    path('', list_bookings, name='list'),
    path('create/', create_booking, name='create'),
    path('<int:pk>/', include([
        path('edit/', edit_booking, name='edit'),
        path('delete/', delete_booking, name='delete')
    ]))
]