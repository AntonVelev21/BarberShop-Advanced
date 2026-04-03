from rest_framework.serializers import ModelSerializer

from api.serializers.barbers import BarberSerializer
from api.serializers.services import ServiceSerializer
from bookings.models import Booking


class BookingSerializer(ModelSerializer):
    barber = BarberSerializer()
    services = ServiceSerializer(many=True)
    class Meta:
        model = Booking
        exclude = ['user_profile', ]
        extra_kwargs = {
            'date_and_hour': {'style': {'input_type': 'text'}}
        }
