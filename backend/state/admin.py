"""This module defines class StateAdmin"""
from django.contrib import admin
from .models import State


admin.site.register(State)
