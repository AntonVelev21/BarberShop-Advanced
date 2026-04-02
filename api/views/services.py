from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from accounts.permissions import HasFullAccessPermission
from api.serializers.services import ServiceSerializer
from services.models import Service


class ListCreateService(ListCreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [HasFullAccessPermission()]
        return [AllowAny()]


class RetrieveUpdateDestroyServiceView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [HasFullAccessPermission()]
        return [AllowAny()]