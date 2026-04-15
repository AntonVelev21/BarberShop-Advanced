from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CASCADE
from services.models import Barber


class Review(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey('accounts.UserProfile', on_delete=CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField(validators=[
        MaxValueValidator(5, message='5 is the maximum rating.'),
        MinValueValidator(0, 'You can not put negative rating!')
    ])
    barber = models.ForeignKey(Barber, related_name='reviews', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)