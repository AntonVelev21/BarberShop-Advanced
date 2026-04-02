from rest_framework import status, permissions
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import HasFullAccessPermission
from api.serializers.barbers import BarberSerializer
from services.models import Barber


class ListCreateBarber(ListCreateAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [HasFullAccessPermission()]
        return [AllowAny()]


class RetrieveUpdateDestroyBarberView(RetrieveUpdateDestroyAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [HasFullAccessPermission()]
        return [AllowAny()]

#class ListCreateBarberApiView(APIView):
#    def get(self, request):
#        barbers = Barber.objects.all()
#        serializer = BarberSerializer(barbers, many=True)
#        return Response(serializer.data, status=status.HTTP_200_OK)
#
#    def post(self, request):
#        serializer = BarberSerializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)



#class RetrieveUpdateDestroyBarberView(APIView):
#    def get(self, request, pk):
#        barber = get_object_or_404(Barber, pk=pk)
#        serializer = BarberSerializer(barber)
#        return Response(serializer.data, status=status.HTTP_200_OK)
#
#    def put(self, request, pk):
#        barber = get_object_or_404(Barber, pk=pk)
#        serializer = BarberSerializer(barber, request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#    def patch(self, request, pk):
#        barber = get_object_or_404(Barber, pk=pk)
#        serializer = BarberSerializer(barber, request.data, partial=True)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#    def delete(self, request, pk):
#        barber = get_object_or_404(Barber, pk=pk)
#        barber.delete()
#        return Response(status=status.HTTP_202_ACCEPTED)

