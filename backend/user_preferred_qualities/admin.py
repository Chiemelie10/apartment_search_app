"""This module defines the class UserPreferredQualityAdmin"""
from django.contrib import admin
from user_preferred_qualities.models import UserPreferredQuality


admin.site.register(UserPreferredQuality)
