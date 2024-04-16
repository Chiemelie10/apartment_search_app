"""This module defines class Amenity."""
from django.db import models


class Amenity(models.Model):
    """This class defines fields of the amenities table in the database."""
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'amenities'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.id} - {self.name}'
