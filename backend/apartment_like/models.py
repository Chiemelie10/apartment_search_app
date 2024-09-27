"""This module defines class ApartmentLike."""
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from apartment.models import Apartment


User = get_user_model()

class ApartmentLike(models.Model):
    """This class defines fields of the model in the database."""
    id = models.CharField(default=uuid4, max_length=36,
                          primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apartment_likes')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='apartment_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        db_table: Name of the table this class creates in the database.
        ordering: The order the instances of this model is displayed on the admin page.
        """
        db_table = 'apartment_likes'
        unique_together = ('user', 'apartment') # Ensures a user can only like an apartment once
        ordering = ['-created_at']

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.id} {self.user.username} {self.apartment.title}'
