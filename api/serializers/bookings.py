from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from bookings.models import Booking


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['user_profile', ]
        extra_kwargs = {
            'date_and_hour': {'style': {'input_type': 'text'}},
            'barber': {'required': False},
            'services': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        barber = validated_data.pop('barber')
        services = validated_data.pop('services')
        user_profile = request.user.user_profile
        booking = Booking.objects.create(user_profile=user_profile, barber=barber, **validated_data)
        booking.services.set(services)
        return booking

    def update(self, instance, validated_data):
        services = validated_data.pop('services', None)
        if services is not None:
            instance.services.set(services)
        if 'barber' in validated_data:
            instance.barber = validated_data.pop('barber')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


    @staticmethod
    def validate_date_and_hour(value):
        entered_date = value
        if entered_date and entered_date < timezone.now():
            raise ValidationError('You cannot book a seat in the past!')
        return entered_date


    def validate(self, attrs):
        date_and_hour = attrs['date_and_hour']
        barber = attrs['barber']

        if date_and_hour and barber:
            if date_and_hour.weekday() == 6:
                raise ValidationError({
                    'date_and_hour': 'Please choose a working day. We work from Monday to Saturday.'
                })

            elif date_and_hour.minute not in [0, 30]:
                raise ValidationError({
                    'date_and_hour': 'Please select a valid time slot (e.g. 10:00 or 10:30).'
                })


            elif date_and_hour.hour < 9 or date_and_hour.hour >= 20:
                raise ValidationError({
                    'date_and_hour': 'Our working hours are between 09:00 and 18:00.'
                })



            else:
                query = Booking.objects.filter(
                    date_and_hour=date_and_hour,
                    barber=barber
                )
                if self.instance and self.instance.pk:
                    query = query.exclude(pk=self.instance.pk)
                if query.exists():
                    raise ValidationError({
                        'date_and_hour': f'Sorry, {barber.first_name} is already booked for this time. Please choose another.'
                    })
        return attrs



