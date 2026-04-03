from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from accounts.permissions import HasFullAccessPermission
from api.serializers.reviews import ReviewSerializer
from reviews.models import Review

"""
To do!
Implement Full CRUD to Review and Booking models;
Config the urls;
Look for creating some custom validators to the project;
Look for some small details or upgrades;
Implement testing logic;
Organize the static or media files and start preparation for deployment
"""
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






