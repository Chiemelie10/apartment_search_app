"""This module defines class CityAdmin"""
from django.contrib import admin
from city.models import City


admin.site.register(City)
