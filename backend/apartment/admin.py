"""This defines class ApartmentAdmin"""
from django.contrib import admin
from .models import Apartment, ApartmentAmenity


admin.site.register(Apartment)
admin.site.register(ApartmentAmenity)
