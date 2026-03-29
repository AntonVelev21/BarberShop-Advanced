from django.db import models
from django.db.models import CASCADE



class Booking(models.Model):
    user_profile = models.ForeignKey('accounts.UserProfile', on_delete=CASCADE, related_name='bookings')
    date_and_hour = models.DateTimeField()
    barber = models.ForeignKey('services.Barber', on_delete=CASCADE, related_name='bookings')
    services = models.ManyToManyField('services.Service', related_name='bookings')

    @property
    def total_price(self):
        total = self.services.aggregate(total=models.Sum('price'))['total'] or 0.00
        return total

    def __str__(self):
        return f"Booking for {self.user_profile.user.username} on {self.date_and_hour.strftime('%d-%m %H:%M')}"
