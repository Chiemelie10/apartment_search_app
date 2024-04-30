"""This module defines class VerificationToken"""
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class VerificationToken(models.Model):
    """This class defines the fields of this class in the database."""
    verification_token = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='verification_token')
    is_for_password_reset = models.BooleanField(default=False)
    is_validated_for_password_reset = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        db_table: Name of the table this class creates in the database.
        ordering: The order the instances of this model is displayed on the admin page.
        """
        db_table = 'verification_tokens'
        ordering = ['-created_at']

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'user: {self.user.username} otp: {self.verification_token}'
