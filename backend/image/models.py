"""This module defines class Image"""
from django.db import models
from apartment.models import Apartment

class Image(models.Model):
    """This class defines the fields of the countries table in the database."""
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='apartment_image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'images'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.id} - {self.image}'
