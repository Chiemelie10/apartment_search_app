"""This module defines class CustomTokenRefreshView"""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.conf import settings
from django.contrib.auth import get_user_model
from user.utils import blacklist_outstanding_tokens


User = get_user_model()

class CustomTokenRefreshView(APIView):
    """This class defines a method that refreshes an access token."""

    @extend_schema(
        request=None,
        responses={200: {'example': {'access': 'access_token_value'}}}
    )
    def post(self, request):
        """
        This method uses refresh token from the cookie to generate new
        access and refresh tokens for a user when a post request is made.\n
        Returns:\n
            On sucess: Access token in the response and refresh token set in the cookie.\n
            On failure: Error message with appropriate http status code.
        """
        # pylint: disable=no-member
        # pylint: disable=broad-exception-caught

        # Get refresh token from cookie.
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token must be set in the cookie.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Verify signature of token.
        try:
            decoded_token = RefreshToken(refresh_token)
            user_id = decoded_token.get('user_id')
            # Blacklist token
            decoded_token.blacklist()
        except TokenError as e:
            if str(e) == 'Token is blacklisted':
                response = RefreshToken(refresh_token, verify=False)
                user_id = response.get('user_id')
                # Blcklist all tokens belonging to the user
                blacklist_outstanding_tokens(user_id)
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Get user object
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Reset user's access and refresh tokens
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        # Defines response body and http status code for successful token refresh.
        response = Response({'access': access_token}, status=status.HTTP_200_OK)

        # Set refresh token in http_only cookie
        response.set_cookie(
            'refresh',
            refresh_token,
            secure=settings.JWT_COOKIE_SECURE,
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            samesite=settings.JWT_COOKIE_SAME_SITE,
            max_age=settings.JWT_COOKIE_MAX_AGE
        )

        # Return response to the client.
        return response
