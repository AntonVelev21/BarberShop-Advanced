from django.forms.models import ModelForm

from accounts.models import UserProfile


class UserProfileCreationForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', )