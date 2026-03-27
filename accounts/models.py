from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='user_profile', null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    rating = models.IntegerField()