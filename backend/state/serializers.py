"""This module defines the serializer classes used for the state app."""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from city.serializers import CityModelSerializer
from apartment.models import Apartment
from .models import State


class StateModelSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the State model
    to be validated when a request is made. This class was created
    specifically for the get_countries and get_states view.
    """

    cities = serializers.SerializerMethodField()

    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = State
        fields = ['id', 'name', 'country', 'cities']

    @extend_schema_field(CityModelSerializer(many=True))
    def get_cities(self, obj):
        """This method returns all cities that have apartments in a corresponding state."""
        #pylint: disable=no-member
        cities = obj.cities.filter(id__in=Apartment.objects.values('city')).distinct()
        return CityModelSerializer(cities, many=True).data


class StateSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the State model
    to be validated when a request is made.
    """

    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = State
        fields = ['id', 'name', 'country']
