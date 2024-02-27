"""This module defines class UserAdmin"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from user.models import UserProfile, UserProfileInterest


User = get_user_model()

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserProfileInterest)
