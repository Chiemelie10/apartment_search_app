"""This module defines class MessageAdmin"""
from django.contrib import admin
from message.models import Message


admin.site.register(Message)
