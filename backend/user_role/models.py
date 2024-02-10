"""This module defines class Role"""
from django.db import models


class UserRole(models.Model):
    """This class defines the columns of the roles table in the database."""
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'user_roles'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        return f'{self.name}'
