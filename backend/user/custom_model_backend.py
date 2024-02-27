"""This module defines class CustomModelBackend."""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class CustomModelBackend(ModelBackend):
    """
    This class defines methods that get and authenticate a user
    from the database.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        This method uses username or email with password to authenticate a user.
        Returns - On success: The user object
                - On Failure: None
        """
        # pylint: disable=invalid-name

        User = get_user_model()

        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password) is False:
            return None
        return user

    def get_user(self, user_id):
        """
        Returns - )n success: A user object if provided user_id exists in the database.
                - On failure: None
        """
        # pylint: disable=invalid-name

        User = get_user_model()

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
