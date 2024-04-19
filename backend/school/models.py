"""This module defines class School"""
from django.db import models
from city.models import City
from state.models import State
from country.models import Country

class School(models.Model):
    """This class defines the fields of the schools table in the database."""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='schools')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='schools')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='schools')
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        db_table: Name of the table this class creates in the database.
        ordering: The order the instances of this model is displayed on the admin page.
        """
        db_table = 'schools'
        ordering =['-created_at']

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.id} - {self.name}'
