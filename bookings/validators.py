from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ClientPhoneValidator:
    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            self.__message = 'Please enter a valid phone!'

        else:
            self.__message = value


    def __call__(self, value):
        clean_phone = value.lstrip('+')

        if not clean_phone.isdigit() or not (9 <= len(clean_phone) <= 13):
            raise ValidationError(self.__message)