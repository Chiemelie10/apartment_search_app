"""This module defines class Apartment."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from apartment.serializers import ApartmentSerializer
from apartment.models import Apartment
from apartment.utils import (
    save_apartment_amenities,
    save_apartment_images,
    delete_apartment_images,
    # reset_advert_exp_time
)


class ApartmentView(APIView):
    """This class defines methods that gets, updates or deletes an apartment object."""

    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser, FormParser]


    def get(self, request, apartment_id):
        """
        This method gets an apartment advert from the database based on provided apartment_id.\n
        Returns:\n
            On success: A http status code of 200 and data of the apartment.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member
        # pylint: disable=unused-argument

        # # Get the requested apartment based on provided apartment_id
        try:
            apartment = Apartment.objects.get(pk=apartment_id)
        except Apartment.DoesNotExist:
            return Response({'error': 'Apartment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # # Reset the time an apartment advert will be taken down
        # if request.user == apartment.user or request.user.is_staff is True:
        #     reset_advert_exp_time(apartment)

        # Serialize the apartment object and return a response.
        serializer = ApartmentSerializer(apartment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, apartment_id):
        """
        This method updates the fields of an apartment advert in the database.\n
        Returns:\n
            On success: A http status code of 200 and the updayed data of the apartment.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member
        # pylint: disable=broad-exception-caught

        # Get the apartment to be updated based on provided apartment_id
        try:
            apartment = Apartment.objects.get(pk=apartment_id)
        except Apartment.DoesNotExist:
            return Response({'error': 'Apartment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure only owners of the apartment advert and staff can update it.
        if request.user != apartment.user and request.user.is_staff is False:
            return Response({'error': 'Resource can only be updated by the owner.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Validate data in request body and return error messages if exception is raised.
        serializer = ApartmentSerializer(
            data=request.data,
            context={
                'request': request,
                'apartment': apartment
            }
        )
        serializer.is_valid(raise_exception=True)

        # Get the value of each field from validated data
        validated_data = serializer.validated_data

        # Reset the time an apartment advert will be taken down
        # extend_time = validated_data.get('extend_time')
        # reset_advert_exp_time(apartment, extend_time)

        country = validated_data.get('country')
        state = validated_data.get('state')
        city = validated_data.get('city')
        school = validated_data.get('school')
        title = validated_data.get('title')
        description = validated_data.get('description')
        image_upload = validated_data.get('image_upload')
        image_delete = validated_data.get('image_delete') # List of image objects
        amenities = validated_data.get('apartmentamenity_set')
        video_link = validated_data.get('video_link')
        is_taken = validated_data.get('is_taken')
        is_taken_time = validated_data.get('is_taken_time')
        is_taken_number = validated_data.get('is_taken_number')
        price = validated_data.get('price')
        listing_type = validated_data.get('listing_type')
        nearest_bus_stop = validated_data.get('nearest_bus_stop')
        approval_status = validated_data.get('approval_status')

        # Set default value for when is_taken is None ie when not included in the request.
        if is_taken is None:
            is_taken = apartment.is_taken

        if is_taken_time is None:
            is_taken_time = apartment.is_taken_time

        if is_taken_number is None:
            is_taken_number = apartment.is_taken_number

        # Set default value for when approval_status is None ie not included in the request.
        if approval_status is None:
            approval_status = apartment.approval_status

        # Update the fields of the apartment with the provided values
        if request.user == apartment.user:
            apartment.country = country
            apartment.state = state
            apartment.city = city
            apartment.school = school
            apartment.title = title
            apartment.description = description
            apartment.video_link = video_link
            apartment.is_taken = is_taken
            apartment.is_taken_time = is_taken_time
            apartment.is_taken_number = is_taken_number
            apartment.price = price
            apartment.listing_type = listing_type
            apartment.nearest_bus_stop = nearest_bus_stop

        if request.user.is_staff is True:
            apartment.approval_status = approval_status

        # Save the changes to the database.
        try:
            apartment.save()
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save amenities for the apartment to the database.
        if request.user == apartment.user and amenities is not None and amenities != []:
            save_apartment_amenities(amenities, apartment)

        # Delete images for the apartment from the database.
        if request.user == apartment.user and image_delete is not None and image_delete != []:
            delete_apartment_images(image_delete)

        # Save images for the apartment to the database.
        if request.user == apartment.user and image_upload is not None and image_upload != []:
            save_apartment_images(image_upload, apartment)

        # serialize apartment object and return a response that includes the serialized data.
        serializer = ApartmentSerializer(apartment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, apartment_id):
        """
        This method partially updates the fields of an apartment advert in the database.\n
        Returns:\n
            On success: A http status code of 200 and the updayed data of the apartment.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member
        # pylint: disable=broad-exception-caught

        # Get the apartment to be updated based on provided apartment_id
        try:
            apartment = Apartment.objects.get(pk=apartment_id)
        except Apartment.DoesNotExist:
            return Response({'error': 'Apartment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure only owners of the apartment advert and staff can update it.
        if request.user != apartment.user and request.user.is_staff is False:
            return Response({'error': 'Resource can only be updated by the owner.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Validate data in request body and return error messages if exception is raised.
        serializer = ApartmentSerializer(
            data=request.data,
            context={
                'request': request,
                'apartment': apartment
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        # Get the value of each field from validated data
        validated_data = serializer.validated_data

        # Reset the time an apartment advert will be taken down
        # extend_time = validated_data.get('extend_time')
        # reset_advert_exp_time(apartment, extend_time)

        if request.user == apartment.user:
            if 'country' in validated_data.keys():
                country = validated_data.get('country')
                apartment.country = country

            if 'state' in validated_data.keys():
                state = validated_data.get('state')
                apartment.state = state

            if 'city' in validated_data.keys():
                city = validated_data.get('city')
                apartment.city = city

            if 'school' in validated_data.keys():
                school = validated_data.get('school')
                apartment.school = school

            if 'title' in validated_data.keys():
                title = validated_data.get('title')
                apartment.title = title

            if 'description' in validated_data.keys():
                description = validated_data.get('description')
                apartment.description = description

            if 'video_link' in validated_data.keys():
                video_link = validated_data.get('video_link')
                apartment.video_link = video_link

            if 'is_taken' in validated_data.keys():
                is_taken = validated_data.get('is_taken')
                apartment.is_taken = is_taken

            if 'is_taken_time' in validated_data.keys():
                is_taken_time = validated_data.get('is_taken_time')
                apartment.is_taken_time = is_taken_time

            if 'is_taken_number' in validated_data.keys():
                is_taken_number = validated_data.get('is_taken_number')
                apartment.is_taken_number = is_taken_number

            if 'price' in validated_data.keys():
                price = validated_data.get('price')
                apartment.price = price

            if 'listing_type' in validated_data.keys():
                listing_type = validated_data.get('listing_type')
                apartment.listing_type = listing_type

            if 'nearest_bus_stop' in validated_data.keys():
                nearest_bus_stop = validated_data.get('nearest_bus_stop')
                apartment.nearest_bus_stop = nearest_bus_stop

            image_upload = None
            if 'image_upload' in validated_data.keys():
                image_upload = validated_data.get('image_upload')

            image_delete = None
            if 'image_delete' in validated_data.keys():
                image_delete = validated_data.get('image_delete') # List of image objects

            amenities = None
            if 'amenities' in validated_data.keys():
                amenities = validated_data.get('apartmentamenity_set')

        if request.user.is_staff is True:
            if 'approval_status' in validated_data.keys():
                approval_status = validated_data.get('approval_status')
                apartment.approval_status = approval_status

        # Save the changes to the database.
        try:
            apartment.save()
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save amenities for the apartment to the database.
        if request.user == apartment.user and amenities is not None and amenities != []:
            save_apartment_amenities(amenities, apartment)

        # Delete images for the apartment from the database.
        if request.user == apartment.user and image_delete is not None and image_delete != []:
            delete_apartment_images(image_delete)

        # Save images for the apartment to the database.
        if request.user == apartment.user and image_upload is not None and image_upload != []:
            save_apartment_images(image_upload, apartment)

        # serialize apartment object and return a response that includes the serialized data.
        serializer = ApartmentSerializer(apartment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={204: None}
    )
    def delete(self, request, apartment_id):
        """
        This method deletes an apartment advert from the database.\n
        Returns:\n
            On success: A http status code of 204.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member
        # pylint: disable=broad-exception-caught

        # Get the apartment to be deleted using the provided apartment_id
        try:
            apartment = Apartment.objects.get(pk=apartment_id)
        except Apartment.DoesNotExist:
            return Response({'error': 'Apartment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure only owners of the apartment advert can delete it.
        if request.user != apartment.user:
            return Response({'error': 'Resource can only be deleted by the owner.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Delete the apartment and return a response.
        apartment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
