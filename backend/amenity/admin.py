"""This defines class AmenityAdmin"""
from django.contrib import admin
from amenity.models import Amenity


admin.site.register(Amenity)
