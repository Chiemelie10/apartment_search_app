"""This module defines class AmenityModelSerializer."""
from rest_framework import serializers
from amenity.models import Amenity


class AmenityModelSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the Amenity model
    to be validated when a request is made.
    """
    # pylint: disable=no-member
    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = Amenity
        fields = '__all__'
