"""This module defines class UserProfileView"""
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from user.serializers import UserProfileSerializer, UserSerializer
from user.models import UserProfileInterest


User = get_user_model()

class UserProfileView(APIView):
    """This class defines methods that gets or updates user profile data"""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
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
                # Get the name of user_interest object from user_profile_interest object
                # and add to a list.
                user_profile_interest_names = []
                for user_profile_interest in user_profile_interests:
                    user_profile_interest_names.append(user_profile_interest.user_interest.name)

                # Add user interest that is not in the list of user_profile_interest_names
                # from database and remove user interests that are in the same list.
                for user_interest in user_interests:
                    if user_interest.name not in user_profile_interest_names:
                        user.profile.interests.add(user_interest)
                    else:
                        user.profile.interests.remove(user_interest)
            else:
                # Add user interests to user profile when the user has
                # no previous captured interests.
                for user_interest in user_interests:
                    user.profile.interests.add(user_interest)

    def get_prev_thumbnail(self, thumbnail, user):
        """
        This method returns existing thumbnail of the user. It prevents
        the thumbnail from being overwritten with null if the user does not
        submit a thumbnail in the request.
        """
        if thumbnail is None:
            thumbnail = user.profile.thumbnail
            if thumbnail is None or thumbnail == '':
                return None
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
        role = validated_data.get('role')
        gender = validated_data.get('gender')
        phone_number = validated_data.get('phone_number')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        thumbnail = validated_data.get('thumbnail')
        thumbnail = self.get_prev_thumbnail(thumbnail, user)

        if role:
            if phone_number is None or gender is None or first_name is None or last_name is None:
                return Response(
                    {
                        'error': 'Gender, phone number, first name or last name '\
                            'should not be None when role is not None.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Delete existing thumbnail if new thumbnail in the request
        existing_thumbnail = user.profile.thumbnail
        if existing_thumbnail:
            existing_thumbnail_path = user.profile.thumbnail.path
            if default_storage.exists(existing_thumbnail_path):
                default_storage.delete(existing_thumbnail_path)

        # Set updated profile
        user.profile.role = role
        user.profile.gender = gender
        user.profile.phone_number = phone_number
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        if thumbnail is not None:
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

        # Update user role if it is in validated data
        if 'role' in validated_data.keys():
            role = validated_data.get('role')
            if role is not None and role.name in ('student', 'agent'):
                for key, value in validated_data.items():
                    if key in ('gender', 'first_name', 'last_name', 'phone_number'):
                        if value is None:
                            return Response(
                                {
                                    'error': f'{key} is required if user role is not '\
                                        'set to None. Delete user role to set it to None.b'
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )
            setattr(user.profile, 'role', role)

        # Update gender value if it is in validated data.
        if 'gender' in validated_data.keys():
            gender = validated_data.get('gender')
            if 'role' not in validated_data.keys():
                # Ensure gender cannot be deleted if role is student or agent.
                if gender is None and str(user.profile.role) in ('student', 'agent'):
                    return Response(
                        {
                            'error': 'Gender is required if user role is not set to None. '\
                                'Delete user role to set it to None.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            setattr(user.profile, 'gender', gender)

        # Update phone number value if it is in validated data.
        if 'phone_number' in validated_data.keys():
            phone_number = validated_data.get('phone_number')
            if 'role' not in validated_data.keys():
                # Ensure phone number cannot be deleted if role is student or agent.
                if phone_number is None and str(user.profile.role) in ('student', 'agent'):
                    return Response(
                        {
                            'error': 'Phone number is required if user role is not '\
                                'set to None. Delete user role to set it to None.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            setattr(user.profile, 'phone_number', phone_number)

        # Update first name value if it is in validated data.
        if 'first_name' in validated_data.keys():
            first_name = validated_data.get('first_name')
            if 'role' not in validated_data.keys():
                # Ensure first name cannot be deleted if role is student or agent.
                if first_name is None and str(user.profile.role) in ('student', 'agent'):
                    return Response(
                        {
                            'error': 'First name is required if user role is not '\
                                'set to None. Delete user role to set it to None.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            setattr(user.profile, 'first_name', first_name)

        # Update last name value if it is in validated data.
        if 'last_name' in validated_data.keys():
            last_name = validated_data.get('last_name')
            if 'role' not in validated_data.keys():
                # Ensure last name cannot be deleted if role is student or agent.
                if last_name is None and str(user.profile.role) in ('student', 'agent'):
                    return Response(
                        {
                            'error': 'Last name is required if user role is not '\
                                'set to None. Delete user role to set it to None.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            setattr(user.profile, 'last_name', last_name)

        # Update thumbnail value if it is in validated data.
        if 'thumbnail' in validated_data.keys():
            thumbnail = validated_data.get('thumbnail')

            # Get existing thumbnail value
            existing_thumbnail = user.profile.thumbnail

            # Delete thumbnail image from the server if it exists
            if existing_thumbnail:
                existing_thumbnail_path = user.profile.thumbnail.path
                if default_storage.exists(existing_thumbnail_path):
                    default_storage.delete(existing_thumbnail_path)

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
