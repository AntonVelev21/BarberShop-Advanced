from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListCreateAPIView

from api.serializers.reviews import ReviewSerializer
from reviews.models import Review


class ListCreateReviewView(LoginRequiredMixin, ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('barber')





