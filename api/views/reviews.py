from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.permissions import HasFullAccessPermission
from api.serializers.reviews import ReviewSerializer
from reviews.models import Review


class ListCreateReviewView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('barber')


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]



class RetrieveUpdateDestroyReviewView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('barber')


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [HasFullAccessPermission()]
        return [AllowAny()]






