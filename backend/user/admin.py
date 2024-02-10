"""This module defines class UserAdmin"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from user.models import UserProfile


User = get_user_model()

admin.site.register(User)
admin.site.register(UserProfile)
