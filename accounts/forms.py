from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework.fields import CharField


class UserCustomCreationForm(UserCreationForm):
    phone_number = CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username']