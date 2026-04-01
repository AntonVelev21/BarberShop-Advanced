from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers.barbers import BarberSerializer
from services.models import Barber


class ListCreateBarber(ListCreateAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

    def get_permissions(self):
        ...


#class ListBarbers(APIView):
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