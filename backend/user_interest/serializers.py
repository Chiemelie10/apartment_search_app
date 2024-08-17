"""This module defines class UserInterestSerializer."""
from rest_framework import serializers
from user_interest.models import UserInterest


class UserInterestSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the UserInterest model
    to be validated when a request is made.
    """
    # pylint: disable=no-member
    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = UserInterest
        fields = ['id', 'name']
