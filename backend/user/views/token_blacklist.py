"""This method defines CustomTokenBlacklistView."""
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema
from user.serializers import TokenBlacklistSerializer
from user.utils import blacklist_outstanding_tokens
from user_suspension.models import UserSuspension


User = get_user_model()

class CustomTokenBlacklistView(APIView):
    """This class defines a method that blacklists a refresh token and suspends a user."""

    serializer_class = TokenBlacklistSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        request={None},
        responses={200: TokenBlacklistSerializer}
    )
    def get(self, request):
        """
        This method returns all currently and previously suspended users in the application.\n
        Returns:\n
            Http status code of 200 and the suspension record of the above stated users.
            It can aslo return empty list If no suspension record exists.\n
        """
        # pylint: disable=unused-argument
        # pylint: disable=no-member

        suspensions = UserSuspension.objects.all()
        serializer = TokenBlacklistSerializer(suspensions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: {'example': {'message': 'User has now been suspended.'}}}
    )
    def post(self, request):
        """
        This method blacklists a user's refresh token and suspends a user for
        the duration in hours submitted by a staff.\n
        Returns:\n
            On sucess: A http status code of 200 and message.\n
            On failure: Error message with appropriate http status code.
        """
        # pylint: disable=no-member
        # pylint: disable=broad-exception-caught

        serializer = TokenBlacklistSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = validated_data.get('user')
        duration = validated_data.get('duration')
        is_permanent = validated_data.get('is_permanent')

        # Set is_permanent to False if None
        if is_permanent is None:
            is_permanent = False

        # Set start and end time
        current_time = timezone.now()
        end_time = None
        if duration is not None:
            end_time = current_time + timedelta(hours=duration)

        try:
            # pylint: disable=unused-variable
            user_suspension = user.suspension
            return Response(
                {
                    'error': 'This account had once been suspended, '\
                    'use the patch method to update the previously created suspension record.'
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        except ObjectDoesNotExist:
            # Add user to the suser_uspensions table
            UserSuspension.objects.create(
                user=user,
                start_time=current_time,
                end_time=end_time,
                duration=duration,
                is_permanent=is_permanent,
                number_of_suspensions=1
            )

        # Blcklist all tokens belonging to the user
        blacklist_outstanding_tokens(user)

        # Set user to inactive
        user.is_active = False
        user.save()

        return Response({'message': 'User has now been suspended.'}, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: {'example': {'message': 'User has now been suspended.'}}}
    )
    def patch(self, request):
        """
        This method updates the data of a suspended user in the user_suspensions table.\n
        Returns:\n
            On sucess: A http status code of 200 and message.\n
            On failure: Error message with appropriate http status code.
        """
        # pylint: disable=no-member
        # pylint: disable=broad-exception-caught

        serializer = TokenBlacklistSerializer(
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = validated_data.get('user')
        duration = validated_data.get('duration')
        is_permanent = validated_data.get('is_permanent')
        has_ended = validated_data.get('has_ended')

        # Set start and end time
        current_time = timezone.now()
        end_time = None
        if duration is not None:
            end_time = current_time + timedelta(hours=duration)

        # Add user to the suser_uspensions table
        try:
            user_suspension = user.suspension

            if has_ended is None or has_ended is False:
                user.suspension.start_time = current_time
                user.suspension.end_time = end_time
                user.suspension.duration = duration
                user.suspension.is_permanent = is_permanent
                user.suspension.number_of_suspensions = user.suspension.number_of_suspensions + 1
                user.suspension.has_ended = False

                # Blcklist all tokens belonging to the user
                blacklist_outstanding_tokens(user)

                # Set user to inactive
                user.is_active = False
                user.suspension.save()
                user.save()

                return Response({'message': 'User has now been suspended.'},
                                status=status.HTTP_200_OK)

            user_suspension.has_ended = True
            user.is_active = True
            user.suspension.save()
            user.save()
            return Response({'message': 'User has now been unsuspended.'},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {
                    'error': 'This account has not been suspended previously, '\
                    'use post method to make the request.'
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
