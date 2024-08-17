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

        user = request.user

        # Confirm user has complete user profile
        first_name = user.profile.first_name
        last_name = user.profile.last_name
        gender = user.profile.gender
        phone_number = user.profile.phone_number
        phone_number_is_verified = user.profile.phone_number_is_verified
        email_is_verified = user.is_verified

        if first_name is None or last_name is None or gender is None or phone_number is None:
            return Response(
                {
                    'error': 'Gender, phone number, first name and last name must be'\
                        'provided in the profile.'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Confirm the user has verified his/her phone number.
        if phone_number_is_verified is False:
            return Response({'error': 'Phone number must be verified'},
                            status=status.HTTP_403_FORBIDDEN)

        # Confirm the user has verified his/her email address.
        if email_is_verified is False:
            return Response({'error': 'Email must be verified'},
                            status=status.HTTP_403_FORBIDDEN)

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
            user=user,
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
            advert_exp_time=timezone.now() + timedelta(weeks=4)
        )

        # Save amenities for the apartment to the database.
        save_apartment_amenities(amenities, apartment)

        # Save images for the apartment to the database.
        save_apartment_images(images, apartment)

        # serialize apartment object and return a response that includes the serialized data.
        serializer = ApartmentSerializer(apartment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
