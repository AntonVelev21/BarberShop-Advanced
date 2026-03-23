from django.conf import settings
from django.db import models
from django.db.models import CASCADE


class Review(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField()
