from django.db import models
from django.db.models import CASCADE



class Booking(models.Model):
    user_profile = models.ForeignKey('accounts.UserProfile', on_delete=CASCADE, related_name='bookings')
    date_and_hour = models.DateTimeField(default=None, null=True, blank=True)
    barber = models.ForeignKey('services.Barber', on_delete=CASCADE, related_name='bookings')
    services = models.ManyToManyField('services.Service', related_name='bookings')

    @property
    def total_price(self):
        total = self.services.aggregate(total=models.Sum('price'))['total'] or 0.00
        return total

    def __str__(self):
        if self.date_and_hour:
            formated_date = self.date_and_hour.strftime('%d-%m %H:%M')
        else:
            formated_date = '(No date set)'
        return f"Booking for {self.user_profile.user.username} on {formated_date}"
