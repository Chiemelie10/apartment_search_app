"""This module defines class UserRoleAdmin"""
from django.contrib import admin
from user_role.models import UserRole


admin.site.register(UserRole)
