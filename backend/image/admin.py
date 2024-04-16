"""This module defines class ImageAdmin"""
from django.contrib import admin
from image.models import Image

admin.site.register(Image)
