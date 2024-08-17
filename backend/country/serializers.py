"""This module defines the serializer classes used for the country app."""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from state.serializers import StateModelSerializer
from apartment.models import Apartment
from .models import Country


class CountryModelSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the Country model
    to be validated when a request is made. This class was created
    specifically for the get_countries and get_states view.
    """
    states = serializers.SerializerMethodField()

    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = Country
        fields = ['id', 'name', 'states']

    @extend_schema_field(StateModelSerializer(many=True))
    def get_states(self, obj):
        """This method returns all states that have apartments."""
        #pylint: disable=no-member
        states = obj.states.filter(id__in=Apartment.objects.values('state')).distinct()
        return StateModelSerializer(states, many=True).data


class CountrySerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the Country model
    to be validated when a request is made.
    """

    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = Country
        fields = ['id', 'name']
