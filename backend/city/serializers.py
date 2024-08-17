"""This module defines the serializer classes used for the city app."""
from rest_framework import serializers
from school.serializers import SchoolModelSerializer
from .models import City


class CityModelSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the City model
    to be validated when a request is made. This class was created
    specifically for the get_countries and get_states view.
    """
    schools = SchoolModelSerializer(read_only=True, required=False, many=True)
    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = City
        fields = ['id', 'name', 'state', 'schools']


class CitySerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the City model
    to be validated when a request is made.
    """
    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = City
        fields = ['id', 'name', 'state']
