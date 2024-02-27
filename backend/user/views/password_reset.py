"""This module defines class PasswordResetView."""
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from user.serializers import PasswordResetSerializer


User = get_user_model()

class PasswordResetView(APIView):
    """
    This class defines a method that resets a user's
    password in the database.
    """

    serializer_class = PasswordResetSerializer

    # Response schema for drf_spectacular
    @extend_schema(
        responses={
            200: {
                'example': {
                    'message': 'Password reset was successful.'
                }
            }
        }
    )
    def post(self, request):
        """
        This method resets a user's password in the database.\n
        Returns:\n
            On success: It returns a http status code of 200 with an appropriate message.\n
            On failure: It returns an error message with a corresponding http status code.
        """
        # pylint: disable=no-member

        # Get refresh token from cookie.
        access_token = request.COOKIES.get('access')
        if not access_token:
            return Response(
                {'error': 'Access token must be set in the cookie.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify signature of refresh token
        try:
            decoded_token = AccessToken(access_token)
            user_id = decoded_token.get('user_id')
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate data in request body and return error messages if exception is raised.
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get password from validated data.
        password = serializer.validated_data.get('password')

        try:
            # Get user object
            user = User.objects.get(pk=user_id)

            # Get token object using related name value in VerificationToken model
            try:
                token = user.verification_token
            except ObjectDoesNotExist:
                return Response({'error': 'Token was not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            # Perform further validation checks on the token
            if token.is_for_password_reset is False or token.is_validated_for_password_reset is False:
                return Response({'error': 'You are not permitted to use this resource.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            # Check if token is used.
            if token.is_used is True:
                return Response({'error': 'Token has been used.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Save the new password for the user.
            user.set_password(password)
            user.save()

            # Update the token as used.
            token.is_used = True
            token.save()

            # Return response to the client.
            message = 'Password reset was successful.'
            return Response({'message': message}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
