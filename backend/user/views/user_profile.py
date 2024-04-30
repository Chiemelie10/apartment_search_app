"""This module defines class UserProfileView"""
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from user.serializers import UserProfileSerializer, UserSerializer
from user.models import UserProfileInterest


User = get_user_model()

class UserProfileView(APIView):
    """This class defines methods that gets or updates user profile data"""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def save_user_interests(self, validated_data, user):
        """This method saves a list of submitted user interests to the database."""
        # pylint: disable=no-member

        # Remove user_interests from validated_data.
        interests = validated_data.get('userprofileinterest_set')

        if interests is not None:
            user_interests = validated_data.pop('userprofileinterest_set')

            # Get all previously saved user interests.
            user_profile_interests = UserProfileInterest.objects.filter(
                user_profile=user.profile
            )
            if user_profile_interests.exists():
                # Add to the database the submitted user_interests that are not in the list
                # user_profile_interests.
                # Also converts from list of dictionaries to a list of user_interest objects.
                user_interest_obj_list = []
                for user_interest in user_interests:
                    user_interest_obj = user_interest['user_interest']
                    user_interest_obj_list.append(user_interest_obj)
                    if user_interest_obj not in user_profile_interests:
                        user.profile.interests.add(user_interest_obj)

                # Delete from the database the user_interests that are not submitted.
                for user_profile_interest in user_profile_interests:
                    if user_profile_interest.user_interest not in user_interest_obj_list:
                        user.profile.interests.remove(user_profile_interest.user_interest)
            else:
                # Add user_interests to a user profile when it has no
                # previous captured user_interests.
                for user_interest in user_interests:
                    user_interest_obj = user_interest['user_interest']
                    user.profile.interests.add(user_interest_obj)

    def get_thumbnail(self, thumbnail, remove_thumbnail, user):
        """
        This method returns existing thumbnail of the user. It prevents
        the thumbnail from being overwritten with null if the user does not
        submit a thumbnail in the request.
        """
        if remove_thumbnail is True:
            # Delete existing thumbnail if new thumbnail in the request
            existing_thumbnail = user.profile.thumbnail
            if existing_thumbnail:
                existing_thumbnail_path = user.profile.thumbnail.path
                if default_storage.exists(existing_thumbnail_path):
                    default_storage.delete(existing_thumbnail_path)
            return None

        if thumbnail is None:
            existing_thumbnail = user.profile.thumbnail
            if existing_thumbnail is None or existing_thumbnail == '':
                return None
            return existing_thumbnail

        # Delete existing thumbnail if new thumbnail in the request
        existing_thumbnail = user.profile.thumbnail
        if existing_thumbnail:
            existing_thumbnail_path = user.profile.thumbnail.path
            if default_storage.exists(existing_thumbnail_path):
                default_storage.delete(existing_thumbnail_path)
        return thumbnail

    @extend_schema(
        responses={200: UserSerializer}
    )
    def get(self, request, user_id):
        """
        This method returns a user profile for the provided user_id.\n
        Args:\n
            user_id: The id of the user that the profile will be viewed.\n
        Returns:\n
            On success: Http status code of 200 and the user's data\n
            On failure: Appropriate http status code and error message.
        """

        try:
            user = User.objects.get(pk=user_id)
            if user != request.user and user.is_staff is False:
                try:
                    has_ended = user.suspension.has_ended
                    if has_ended is False:
                        return Response(
                            {
                                'error': 'This account is suspended.'
                            },
                            status=status.HTTP_403_FORBIDDEN
                        )
                except ObjectDoesNotExist:
                    pass
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={200: UserSerializer}
    )
    def put(self, request, user_id):
        """
        This method saves the profile data of a user in the database.\n
        Args:\n
            user_id: The id of the user\n
        Returns:\n
            On success: Http status code of 200 and the user's data\n
            On failure: Appropriate http status code and error message.
        """
        # pylint: disable=no-member

        # compare user making the request to user that owns the profile to be viewed.
        user = request.user
        if user.id != user_id:
            return Response({'error': 'Profile can only be updated by the owner.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Validate data in request body and return error messages if exception is raised.
        serializer = UserProfileSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Get updated values from validated data
        gender = validated_data.get('gender')
        phone_number = validated_data.get('phone_number')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        remove_thumbnail = validated_data.get('remove_thumbnail')
        thumbnail = validated_data.get('thumbnail')
        thumbnail = self.get_thumbnail(thumbnail, remove_thumbnail, user)

        # Check if user has active Apartment class objects in the database
        # return a 403 http response if the user does.
        apartments = user.apartments.filter(
            is_taken=False,
            advert_days_left__gt=0,
            approval_status__in=['accepted', 'pending']
        )
        if apartments.exists():
            if gender is None or phone_number is None or first_name is None or last_name is None:
                return Response(
                    {
                        'error': 'Gender, phone number, first name or last name is '\
                            'required when a user has active apartment adverts.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        # Set phone_number_is_verified to False if phone number has been changed
        if user.profile.phone_number != phone_number:
            user.profile.phone_number_is_verified = False

        # Set updated profile
        user.profile.gender = gender
        user.profile.phone_number = phone_number
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.thumbnail = thumbnail

        # Save submitted user interests.
        self.save_user_interests(validated_data, user)

        user.profile.save()

        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: UserSerializer}
    )
    def patch(self, request, user_id):
        """
        This method partially updates one or more profile data of a user.\n
        Args:\n
            user_id: The id of the user\n
        Returns:\n
            On success: Http status code of 200 and the user's data\n
            On failure: Appropriate http status code and error message.
        """
        # pylint: disable=no-member

        # compare user making the request to user that owns the profile to be viewed.
        user = request.user
        if user.id != user_id:
            return Response({'error': 'Profile can only be updated by the owner.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Validate data in request body and return error messages if exception is raised.
        serializer = UserProfileSerializer(
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Check if user has active Apartment class objects in the database
        # set has_apartment_ad to True if the user does.
        has_active_ad = False
        apartments = user.apartments.filter(
            is_taken=False,
            advert_days_left__gt=0,
            approval_status__in=['accepted', 'pending']
        )
        if apartments.exists():
            has_active_ad = True

        # Update gender value if it is in validated data.
        if 'gender' in validated_data.keys():
            gender = validated_data.get('gender')

            # Ensure gender cannot be set to None when a user has active apartment advert(s).
            if has_active_ad is True and gender is None:
                return Response(
                    {
                        'error': 'The field "gender" is required when a user has active '\
                            'apartment adverts.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            setattr(user.profile, 'gender', gender)

        # Update phone number value if it is in validated data.
        if 'phone_number' in validated_data.keys():
            phone_number = validated_data.get('phone_number')
            # Ensure phone number cannot be set to None when a user has
            # active apartment advert(s).
            if has_active_ad is True and phone_number is None:
                return Response(
                    {
                        'error': 'The field "phone_number" is required when a user '\
                            'has active apartment adverts.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # Set phone_number_is_verified to False if phone number has been changed
            if user.profile.phone_number != phone_number:
                setattr(user.profile, 'phone_number_is_verified', False)
            setattr(user.profile, 'phone_number', phone_number)

        # Update first name value if it is in validated data.
        if 'first_name' in validated_data.keys():
            first_name = validated_data.get('first_name')
            # Ensure first name cannot be set to None when a user has
            # active apartment advert(s).
            if has_active_ad is True and first_name is None:
                return Response(
                    {
                        'error': 'The field "first_name" is required when a user '\
                            'has active apartment adverts.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            setattr(user.profile, 'first_name', first_name)

        # Update last name value if it is in validated data.
        if 'last_name' in validated_data.keys():
            last_name = validated_data.get('last_name')
            # Ensure last name cannot be set to None when a user has
            # active apartment advert(s).
            if has_active_ad is True and last_name is None:
                return Response(
                    {
                        'error': 'The field "last_name" is required when a user '\
                            'has active apartment adverts.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            setattr(user.profile, 'last_name', last_name)

        # Update thumbnail value if it is in validated data.
        if 'thumbnail' in validated_data.keys():
            thumbnail = validated_data.get('thumbnail')

            remove_thumbnail = False
            if 'remove_thumbnail' in validated_data.keys():
                remove_thumbnail = validated_data.get('remove_thumbnail', False)

            thumbnail = self.get_thumbnail(thumbnail, remove_thumbnail, user)

            setattr(user.profile, 'thumbnail', thumbnail)

        # Update email if it is in validated data
        if 'email' in validated_data.keys():
            email = validated_data.get('email')
            setattr(user, 'email', email)
            setattr(user, 'is_verified', False)

        # Delete submitted user interests.
        if 'userprofileinterest_set' in validated_data.keys():
            self.save_user_interests(validated_data, user)


        # Save the changes to the database and return response.
        user.save()
        user.profile.save()
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={204: None}
    )
    def delete(self, request, user_id):
        """
        This method deletes the account of a user identified by the user_id.\n
        Args:\n
            user_id: The id of the user that the data will be deleted.\n
        Returns:\n
            On success: Http status code of 204 with no response in the body.\n
            On failure: Appropriate http status code and error message.
        """
        user = request.user
        if user.id != user_id:
            return Response({'error': 'Account can only be deleted by the owner.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get refresh token from cookie.
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token must be set in the cookie.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Verify signature of refresh token and blacklist it if no error
        try:
            decoded_token = RefreshToken(refresh_token)
            decoded_token.blacklist()
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
