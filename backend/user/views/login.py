"""This module defines class LoginView"""
import humanize
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from user.serializers import LoginSerializer
from user.utils import get_tokens_for_user, blacklist_outstanding_tokens


class LoginView(APIView):
    """This class defines a method that log a user into the application."""

    serializer_class = LoginSerializer

    def get_request_user(self, request, validated_data):
        """
        Args - validated_data: A dictionary containing the validated data in the
                               body of the request.
             - request: The request object.

        Returns - On success: The user object
                - On failure: None
        """
        password = validated_data.get('password')
        username = validated_data.get('username')
        email = validated_data.get('email')

        if username:
            user = authenticate(request, username=username, password=password)
        elif email:
            user = authenticate(request, username=email, password=password)

        if user is None:
            return None
        return user

    # Response schema for drf_spectacular
    @extend_schema(
        responses={
            200: {
                'example': {
                    'message': 'User login was successful.',
                    'access': 'access_token_value'
                }
            }
        }
    )
    def post(self, request):
        """
        This class defines a method that logs a user into the application.\n
        Returns:\n
            On success: A jwt access token in the body of the response and a jwt
                        refresh token set in the cookie.\n
            On failure: An error message with a corresponding http status
                        code.
        """
        # Validate data in request body and return error messages if exception is raised.
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        # Authenticate user
        user = self.get_request_user(request, validated_data)
        if user is None:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if user is not active
        if user.is_active is False:
            # Check if the reason for being inactive is due to suspension
            try:
                current_time = timezone.now()
                end_time = user.suspension.end_time
                if end_time is not None:
                    # Prevent user from logging in if suspension endtime
                    # has not been equaled or exceeded.
                    if current_time < end_time:
                        time_difference = end_time - current_time
                        readable_time_difference = humanize.naturaldelta(time_difference)
                        return Response(
                            {
                                'error': f'Account was suspended, '
                                         f'time remaining is {readable_time_difference}.'
                            },
                            status=status.HTTP_403_FORBIDDEN
                        )
                    # End user suspension and set user to active
                    user.suspension.has_ended = True
                    user.suspension.save()
                    user.is_active = True

                # Prevent user from logging in if account is permanently suspended.
                if user.suspension.is_permanent is True and user.suspension.has_ended is False:
                    return Response(
                        {
                            'error': 'Account has been permanently suspended.'
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
            except ObjectDoesNotExist:
                pass

        # Blacklist all outstanding refresh token for the user
        blacklist_outstanding_tokens(user)

        # Generate access and refresh tokens for user
        tokens = get_tokens_for_user(user)
        access_token = tokens.get('access')
        refresh_token = tokens.get('refresh')

        if access_token is None or refresh_token is None:
            return Response({'error': 'Failed to generate refresh or access token.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Update time of user's last login
        user.last_login = timezone.now()
        user.save()

        # Define response body and http status code for successful login
        response = Response(
            {
                'message': 'User login was successful.',
                'access': access_token
            },
            status=status.HTTP_200_OK
        )

        # Set refresh token in the cookie
        response.set_cookie(
            'refresh',
            refresh_token,
            secure=settings.JWT_COOKIE_SECURE,
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            samesite=settings.JWT_COOKIE_SAME_SITE,
            max_age=settings.JWT_COOKIE_MAX_AGE
        )

        # Return response
        return response
