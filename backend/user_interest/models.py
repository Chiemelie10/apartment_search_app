"""This module defines class UserInterest."""
from django.db import models


class UserInterest(models.Model):
    """This class defines fields of the model in the database."""
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'user_interests'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        return f'{self.name}'
