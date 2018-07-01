from django.contrib import admin
from .models import Passenger
# Register your models here.

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'survived', 'ticket_class', 'embarked')