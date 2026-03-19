from django.contrib import admin

from services.models import Service, Barber


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    ...

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    ...