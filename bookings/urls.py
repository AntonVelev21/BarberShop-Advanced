from django.urls.conf import path, include

from bookings.views import ListBookingsView, CreateBookingView, EditBookingView, DeleteBookingView

app_name = 'bookings'

urlpatterns = [
    path('', ListBookingsView.as_view(), name='list'),
    path('create/', CreateBookingView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('edit/', EditBookingView.as_view(), name='edit'),
        path('delete/', DeleteBookingView.as_view(), name='delete')
    ]))
]