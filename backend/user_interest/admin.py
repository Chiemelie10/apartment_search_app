"""This module defines the class UserInterestAdmin"""
from django.contrib import admin
from user_interest.models import UserInterest


admin.site.register(UserInterest)
