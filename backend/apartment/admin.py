"""This defines class ApartmentAdmin"""
from django.contrib import admin
from .models import Apartment, ApartmentAmenity, ApartmentUserPreferredQuality


admin.site.register(Apartment)
admin.site.register(ApartmentAmenity)
admin.site.register(ApartmentUserPreferredQuality)
