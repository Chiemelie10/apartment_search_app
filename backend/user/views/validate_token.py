"""This module defines classes for validation of email and password tokens."""
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from drf_spectacular.utils import extend_schema
from user.serializers import VerificationTokenSerializer
from user.utils import is_token_expired
from user_verification_token.models import VerificationToken


class ValidateEmailVerificationTokenView(APIView):
    """
    This class defines a method that handles validation of token
    for verifying email address.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = VerificationTokenSerializer

    # Response schema for drf_spectacular
    @extend_schema(
        responses={
            200: {
                'example': {
                    'message': 'Email verified successfully.'
                }
            }
        }
    )
    def post(self, request):
        """
        This method verifies a user's email address using a One Time Password.\n
        Returns:\n
            On sucess: A success message to the client.\n
            On failure: The reason of failure to the client.
        """
        # pylint: disable=no-member

        # Validate data in request body and return error messages if exception is raised.
        serializer = VerificationTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get verification token (string) from validated data.
        verification_token = serializer.validated_data.get('verification_token')

        try:
            # Get verification token (object) from database.
            token = VerificationToken.objects.get(verification_token=verification_token)
            user = token.user # Get user object from token

            # Check if token has been used.
            if token.is_used is True:
                return Response({'error': 'Token has been used.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if account has already been verified.
            if user.is_verified is True:
                return Response({'error': 'Account has already been verified.'},
                                status=status.HTTP_400_BAD_REQUEST)

        except VerificationToken.DoesNotExist:
            return Response({'error': 'Token is incorrect.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if OTP has expired.
        token_expired = is_token_expired(token, settings.OTP_EXP_TIME)

        if token_expired is True:
            return Response({'error': 'Token has expired.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the is_verified field of the User model and save.
        user.is_verified = True
        user.save()

        # Update the is_used field of the VerificationToken model and save.
        token.is_used = True
        token.save()

        # Return a success response to the client.
        message = 'Email verified successfully.'
        return Response({'message': message}, status=status.HTTP_200_OK)


class ValidatePasswordResetTokenView(APIView):
    """
    This class defines a method that validates One Time
    Password (OTP) for password reset.
    """

    serializer_class = VerificationTokenSerializer

    # Response schema for drf_spectacular
    @extend_schema(
        responses={
            200: {
                'example': {
                    'message': 'Token for password reset verified successfully.'
                }
            }
        }
    )
    def post(self, request):
        """
        This method validates a token for password reset.\n
        Returns:\n
            On sucess: A success message to the client.\n
            On failure: The reason for the failure to the client.
        """
        # pylint: disable=no-member

        # Validate data in request body and return error messages if exception is raised.
        serializer = VerificationTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get verification token (string) from validated data.
        verification_token = serializer.validated_data.get('verification_token')

        try:
            # Get verification token (object) from database.
            token = VerificationToken.objects.get(verification_token=verification_token)
        except VerificationToken.DoesNotExist:
            return Response({'error': 'Token is incorrect.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if token is used.
        if token.is_used is True:
            return Response({'error': 'Token has been used.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if token has expired.
        token_expired = is_token_expired(token, settings.OTP_EXP_TIME)

        if token_expired is True:
            return Response({'error': 'Token has expired.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Generate access token for user for password reset
        access_token = AccessToken.for_user(token.user)

        # Define the response body that will be returned to the client
        message = 'Token for password reset verified successfully.'
        response = Response({'message': message}, status=status.HTTP_200_OK)

        # Set access token in the cookie for the response
        response.set_cookie(
            'access',
            access_token,
            secure=settings.JWT_COOKIE_SECURE,
            httponly=settings.JWT_COOKIE_HTTP_ONLY,
            samesite=settings.JWT_COOKIE_SAME_SITE,
            max_age=settings.PASSWORD_RESET_COOKIE_MAX_AGE
        )

        # Update is_validated_for_password_reset field in VerificationToken model and save.
        token.is_validated_for_password_reset = True
        token.save()

        return response
