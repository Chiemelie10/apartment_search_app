"""This module defines class LogoutView."""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class LogoutView(APIView):
    """This class defines a method that logs a user out of the application."""

    permission_classes = [IsAuthenticated]

    # request and response schema for drf_spectacular
    @extend_schema(
        request=None,
        responses={204: None}
    )
    def post(self, request):
        """
        This method logs a user out of the application.\n
        Returns:\n
                On sucess: Http status code of 204 with no data in the response body.\n
                On failure: An error message with an appropriate http status code.
        """
        # pylint: disable=broad-exception-caught

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
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
