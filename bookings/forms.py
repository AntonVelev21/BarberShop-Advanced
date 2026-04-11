from django.utils import timezone

from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from bookings.models import Booking
"""
To do:
Implement custom calendar with available booking hours fot the chosen day

"""

class BaseBookingForm(ModelForm):
    class Meta:
        model = Booking
        exclude = ['user_profile', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_time_field = self.fields['date_and_hour']
        date_time_field.widget.input_type = 'datetime-local'


    def clean_date_and_hour(self):
        entered_date = self.cleaned_data.get('date_and_hour')
        if entered_date and entered_date < timezone.now():
            raise ValidationError('You cannot book a seat in the past!')
        return entered_date


    def clean(self):
        cleaned_data = super().clean()
        date_and_hour = cleaned_data.get('date_and_hour')
        barber = cleaned_data.get('barber')

        if date_and_hour and barber:
            if date_and_hour.weekday() == 6:
                self.add_error('date_and_hour', 'Please choose a working day. We work from Monday to Saturday.')


            elif date_and_hour.minute not in [0, 30]:
                self.add_error('date_and_hour', 'Please select a valid time slot (e.g. 10:00 or 10:30).')


            elif date_and_hour.hour < 9 or date_and_hour.hour >= 20:
                self.add_error('date_and_hour', 'Our working hours are between 09:00 and 18:00.')

            else:
                is_booked = Booking.objects.filter(
                    date_and_hour=date_and_hour,
                    barber=barber
                ).exists()

                if is_booked:
                    self.add_error('date_and_hour', f'Sorry, {barber.first_name} is already booked for this time. Please choose another.')

        return cleaned_data



class BookingCreateForm(BaseBookingForm):
    ...


class BookingEditForm(BaseBookingForm):
    ...


class BookingDeleteForm(BaseBookingForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True