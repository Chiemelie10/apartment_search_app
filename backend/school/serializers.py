"""This module defines the serializer classes used for the school app."""
from rest_framework import serializers
from .models import School


class SchoolModelSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the School model
    to be validated when a request is made.
    """

    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = School
        fields = ['id', 'name', 'country', 'state', 'city']
