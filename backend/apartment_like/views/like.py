"""This module defines class Like."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from apartment_like.models import ApartmentLike
from apartment_like.serializers import ApartmentLikeSerializer


class Like(APIView):
    """
        This class defines methods that gets, creates, updates and deletes like objects
        from the database.
    """
    serializer_class = ApartmentLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=ApartmentLikeSerializer,
        responses={201: ApartmentLikeSerializer}
    )
    def post(self, request, apartment_id):
        """
        This method creates and saves apartment like reaction in the database.\n
        Returns:\n
            On success: A http status code of 201 and id of the user and apartment.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member
        user = request.user

        # Validate data in request body and return error messages if exception is raised.
        serializer = ApartmentLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the value of each field from validated data
        validated_data = serializer.validated_data

        apartment = validated_data.get('apartment')

        # Create and save apartment like reaction in the database.
        apartment = ApartmentLike.objects.create(
            user=user,
            apartment=apartment_id,
        )

        # serialize apartment like reaction object and return a response
        # that includes the serialized data.
        serializer = ApartmentLikeSerializer(apartment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
