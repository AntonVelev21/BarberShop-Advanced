from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from services.models import Barber


class BarberSerializer(ModelSerializer):
    class Meta:
        model = Barber
        exclude = ['slug']
