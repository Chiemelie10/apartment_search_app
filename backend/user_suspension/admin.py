"""This module defines class UserSuspensionAdmin"""
from django.contrib import admin
from .models import UserSuspension


admin.site.register(UserSuspension)
