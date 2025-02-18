"""This module defines class Country"""
from uuid import uuid4
from django.db import models

class Country(models.Model):
    """This class defines the fields of the countries table in the database."""
    id = models.CharField(default=uuid4, max_length=36,
                          unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        db_table: Name of the table this class creates in the database.
        verbose_name_plural: Plural form of human readable name of the model in the admin page.
        ordering: The order the instances of this model is displayed on the admin page.
        """
        db_table = 'countries'
        verbose_name_plural = 'Countries'
        ordering =['-created_at']

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.id} - {self.name}'
