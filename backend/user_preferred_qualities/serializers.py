"""This module defines class UserPreferredQualitySerializer."""
from rest_framework import serializers
from user_preferred_qualities.models import UserPreferredQuality


class UserPreferredQualitySerializer(serializers.ModelSerializer):
    """
    This class defines the class attributes of the UserPreferredQuality model
    to be validated when a request is made.
    """
    # pylint: disable=no-member
    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = UserPreferredQuality
        fields = ['id', 'name']
