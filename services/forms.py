from django.forms.models import ModelForm
from services.models import Barber, Service


class BaseBarberForm(ModelForm):
    class Meta:
        model = Barber
        exclude = ['slug']


class BarberCreateForm(BaseBarberForm):
    ...


class BarberEditForm(BaseBarberForm):
    ...


class BarberDeleteForm(BaseBarberForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True


class BaseServiceForm(ModelForm):
    class Meta:
        model = Service
        exclude = ['slug']


class ServiceCreateForm(BaseServiceForm):
    ...


class ServiceEditForm(BaseServiceForm):
    ...


class ServiceDeleteForm(BaseServiceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True