"""This module defines class ImageSerializer."""
from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    """This class defines the fields of the Image model to be validated or serialized."""
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = Image
        fields = '__all__'

    def to_representation(self, instance):
        """This method defines fields returned when request method is GET or POST"""
        representation = super().to_representation(instance)
        representation.pop('created_at', None)
        representation.pop('updated_at', None)
        representation.pop('apartment', None)

        return representation
