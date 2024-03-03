"""This module defines class LoginView"""
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate
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
        serializer = LoginSerializer(data=request.data)

        # Validate data in request body and return error messages if exception is raised.
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        # Authenticate user
        user = self.get_request_user(request, validated_data)
        if user is None:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

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
