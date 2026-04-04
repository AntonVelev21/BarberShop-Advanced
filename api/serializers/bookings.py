from django.shortcuts import get_list_or_404
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer

from api.serializers.barbers import BarberSerializer
from api.serializers.services import ServiceSerializer
from bookings.models import Booking
from services.models import Barber, Service


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['user_profile', ]
        extra_kwargs = {
            'date_and_hour': {'style': {'input_type': 'text'}}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        barber = validated_data.pop('barber')
        services = validated_data.pop('services')
        user_profile = request.user.user_profile
        booking = Booking.objects.create(user_profile=user_profile, barber=barber, **validated_data)
        booking.services.set(services)
        return booking


    def update(self, instance, validated_data):
        barber = validated_data.pop('barber', instance.barber)
        services = validated_data.pop('services', None)
        instance.barber = barber
        if services:
             instance.services.set(services)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        return instance

