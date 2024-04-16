"""This module defines class CreateApartmentView."""
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from apartment.models import Apartment
from apartment.utils import (
    save_apartment_amenities,
    save_apartment_images
)
from apartment.serializers import ApartmentSerializer


class CreateApartmentView(APIView):
    """This class defines methods that gets, updates or deletes an apartment object."""

    permission_classes = [IsAuthenticated]
    serializer_class = ApartmentSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @extend_schema(
        request=ApartmentSerializer,
        responses={201: ApartmentSerializer}
    )
    def post(self, request):
        """
        This method creates and saves apartment advert in the database.\n
        Returns:\n
            On success: A http status code of 201 and data of the apartment.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member

        # Validate data in request body and return error messages if exception is raised.
        serializer = ApartmentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Get the value of each field from validated data
        validated_data = serializer.validated_data
        country = validated_data.get('country')
        state = validated_data.get('state')
        city = validated_data.get('city')
        school = validated_data.get('school')
        title = validated_data.get('title')
        description = validated_data.get('description')
        images = validated_data.get('image_upload')
        amenities = validated_data.get('apartmentamenity_set')
        video_link = validated_data.get('video_link')
        price = validated_data.get('price')
        listing_type = validated_data.get('listing_type')
        nearest_bus_stop = validated_data.get('nearest_bus_stop')

        # Create and save apartment in the database.
        apartment = Apartment.objects.create(
            user=request.user,
            country=country,
            state=state,
            city=city,
            school=school,
            title=title,
            description=description,
            video_link=video_link,
            price=price,
            listing_type=listing_type,
            nearest_bus_stop=nearest_bus_stop,
            advert_days_left=28,
            advert_exp_time=timezone.now() + timedelta(weeks=4)
        )

        # Save amenities for the apartment to the database.
        save_apartment_amenities(amenities, apartment)

        # Save images for the apartment to the database.
        save_apartment_images(images, apartment)

        # serialize apartment object and return a response that includes the serialized data.
        serializer = ApartmentSerializer(apartment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
