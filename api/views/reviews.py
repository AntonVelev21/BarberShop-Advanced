from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from accounts.permissions import HasFullAccessPermission
from api.serializers.reviews import ReviewSerializer
from reviews.models import Review


class ListCreateReviewView(LoginRequiredMixin, ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('barber')



class RetrieveUpdateDestroyReviewView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('barber')


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [HasFullAccessPermission()]
        return [AllowAny()]






