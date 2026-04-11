from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0, message='Price can not be negative!')
    ])
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    description = models.TextField()
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    image_url = models.URLField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.price} euro)"



class Barber(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image_url = models.URLField()
    bio = models.TextField()
    years_of_experience = models.IntegerField()
    slug = models.SlugField(max_length=50, unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.first_name}-{self.last_name}', allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'