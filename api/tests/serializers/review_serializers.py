from django.contrib.auth.models import User
from django.test import TestCase

from api.serializers.reviews import ReviewSerializer
from reviews.models import Review
from services.models import Barber



class ReviewSerializerTests(TestCase):
    ...