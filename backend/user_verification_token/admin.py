"""This module defines class VerificationTokenAdmin"""
from django.contrib import admin
from user_verification_token.models import VerificationToken


admin.site.register(VerificationToken)
