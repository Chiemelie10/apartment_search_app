# This module defines class UserPreferredQuality

from django.db import models


class UserPreferredQuality(models.Model):
    """This class defines fields of the model in the database."""
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        db_table: Name of the table this class creates in the database.
        ordering: The order the instances of this model is displayed on the admin page.
        """
        db_table = 'user_preferred_qualities'
        verbose_name_plural = 'User preferred qualities'
        ordering = ['-created_at']

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.id} - {self.name}'
