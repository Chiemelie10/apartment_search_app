"""This module defines class City"""
from django.db import models
from state.models import State

class City(models.Model):
    """This class defines the fields of the cities table in the database."""
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'cities'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.id} - {self.name}'
