"""This module defines class ApartmentLikeSerializer."""
from rest_framework import serializers
from apartment_like.models import ApartmentLike


class ApartmentLikeSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the ApartmentLIke model
    to be validated when a request is made.
    """
    # pylint: disable=no-member
    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = ApartmentLike
        fields = ['id', 'user', 'apartment']
