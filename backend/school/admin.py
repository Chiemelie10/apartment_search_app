"""This module defines class SchoolAdmin"""
from django.contrib import admin
from school.models import School


admin.site.register(School)
