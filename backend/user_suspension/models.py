"""This module defines class UserSuspension"""
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSuspension(models.Model):
    """This class defines the fields of the user_suspensions table."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='suspension')
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True)
    is_permanent = models.BooleanField(default=False)
    has_ended = models.BooleanField(default=False)
    number_of_suspensions = models.IntegerField(default=0)

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'user_suspensions'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.user.id} -- {self.user.username} -- {self.number_of_suspensions}'
