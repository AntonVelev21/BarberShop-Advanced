from django.db import models
from django.db.models.deletion import SET_NULL

from bookings.validators import ClientPhoneValidator


class Booking(models.Model):
    client_name = models.CharField(max_length=50)
    client_phone = models.CharField(max_length=20, validators=[
        ClientPhoneValidator()
    ])
    date_and_hour = models.DateTimeField()
    barber = models.ForeignKey('services.Barber', on_delete=SET_NULL, null=True, blank=True, related_name='bookings')
    services = models.ManyToManyField('services.Service', related_name='bookings')

    @property
    def total_price(self):
        total = self.services.aggregate(total=models.Sum('price'))['total'] or 0.00
        return total

    def __str__(self):
        return f"Booking for {self.client_name} on {self.date_and_hour.strftime('%d-%m %H:%M')}"
