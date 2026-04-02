from rest_framework.serializers import ModelSerializer

from services.models import Service


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        exclude = ['slug']