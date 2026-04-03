from rest_framework.serializers import ModelSerializer

from api.serializers.barbers import BarberSerializer
from reviews.models import Review
from services.models import Barber


class ReviewSerializer(ModelSerializer):
    barber = BarberSerializer()
    class Meta:
        model = Review
        exclude = ('author', )


    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user.user_profile
        barber_data = validated_data.pop('barber')
        barber = Barber.objects.create(**barber_data)
        return Review.objects.create(barber=barber, author=author, **validated_data)


