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


    def update(self, instance, validated_data):
        if 'barber' in validated_data:
            barber_data = validated_data.pop('barber')
            for attr, value in barber_data.items():
                setattr(instance.barber, attr, value)
                instance.barber.save()

        request = self.context.get('request')
        author = request.user.user_profile
        instance.author = author
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance












