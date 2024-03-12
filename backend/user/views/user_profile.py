"""This module defines class UserProfileView"""
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
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
    """This class defines a post method that captures user profile data"""

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

            # Covert interest objects submitted by the user to their names and save in a list.
            user_interest_names = []
            for user_interest in user_interests:
                user_interest_names.append(user_interest.name)

            # Get all previously saved user interests and delete
            # each that is not among the newly submitted user interests.
            user_profile_interests = UserProfileInterest.objects.filter(
                user_profile=user.profile
            )
            if user_profile_interests.exists():
                for user_profile_interest in user_profile_interests:
                    if user_profile_interest.user_interest.name not in user_interest_names:
                        user.profile.interests.remove(user_profile_interest.user_interest)

            # Save newly submitted user interests to the database.
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
    def put(self, request, user_id):
        """
        This method saves user profile data in the database.\n
        Args:\n
            user_id: The id of the user\n
        Returns:\n
            On success: Http status code of 201 and the user's data\n
            On failure: Appropriate http status code and error message.
        """
        # pylint: disable=no-member

        # compare user making the request to user that owns the profile to be viewed.
        user = request.user
        if user.id != user_id:
            return Response({'error': 'User profile can only be created by the owner.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Validate data in request body and return error messages if exception is raised.
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Save submitted user interests.
        self.save_user_interests(validated_data, user)

        # Get updated values from validated data
        role = validated_data.get('role')
        gender = validated_data.get('gender')
        phone_number = validated_data.get('phone_number')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        thumbnail = validated_data.get('thumbnail')
        thumbnail = self.get_prev_thumbnail(thumbnail, user)

        # Delete existing thumbnail if new thumbnail in the request
        existing_thumbnail = user.profile.thumbnail
        if existing_thumbnail:
            existing_thumbnail_path = user.profile.thumbnail.path
            if default_storage.exists(existing_thumbnail_path):
                default_storage.delete(existing_thumbnail_path)

        # Set updated profile
        user.profile.role = role
        user.profile.gender = gender
        # user_profile.interests = interests
        user.profile.phone_number = phone_number
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        if thumbnail is not None:
            user.profile.thumbnail = thumbnail

        user.profile.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
