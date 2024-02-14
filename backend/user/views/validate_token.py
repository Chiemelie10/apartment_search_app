"""This module defines classes for validation of email and password tokens."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from user.serializers import VerificationTokenSerializer
from user.utils import is_token_expired
from user_verification_token.models import VerificationToken


class ValidateEmailVerificationTokenView(APIView):
    """
    This class defines a method that handles validation of token
    for verifying email address.
    """

    serializer_class = VerificationTokenSerializer

    def post(self, request):
        """
        This method sets the is_verified field of the User model to true.

        returns:
            - On sucess: A success message to the client.
            - On failure: The reason for the failure to the client.
        """
        # pylint: disable=no-member

        serializer = VerificationTokenSerializer(data=request.data)

        if serializer.is_valid():
            verification_token = serializer.validated_data.get('verification_token')

            try:
                token = VerificationToken.objects.get(verification_token=verification_token)
                user = token.user

                if user.is_verified is True:
                    return Response({'error': 'Account has already been verified.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if token.is_used is True:
                    return Response({'error': 'Token has been used.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            except VerificationToken.DoesNotExist:
                return Response({'error': 'Token is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            token_expired = is_token_expired(token, 600)

            if token_expired is True:
                return Response({'error': 'Token has expired'},
                                status=status.HTTP_400_BAD_REQUEST)

            user.is_verified = True
            user.save()

            token.is_used = True
            token.save()

            message = 'Email verified successfully.'
            return Response({'message': message}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidatePasswordResetTokenView(APIView):
    """This class defines a method that validates token for password reset."""

    serializer_class = VerificationTokenSerializer

    def post(self, request):
        """
        This method validates a token for password reset.

        returns:
            - On sucess: A success message to the client and the submitted One Time Password.
            - On failure: The reason for the failure to the client.
        """
        # pylint: disable=no-member

        serializer = VerificationTokenSerializer(data=request.data)

        if serializer.is_valid():
            verification_token = serializer.validated_data.get('verification_token')

            try:
                token = VerificationToken.objects.get(verification_token=verification_token)
            except VerificationToken.DoesNotExist:
                return Response({'error': 'Token is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            token_expired = is_token_expired(token, 600)

            if token_expired is True:
                return Response({'error': 'Token has expired'},
                                status=status.HTTP_400_BAD_REQUEST)

            token.otp_submission_time = timezone.now()
            token.is_validated_for_password_reset = True
            token.save()
            message = 'Token for password reset verified successfully.'
            return Response({'message': message, 'verification_token': verification_token},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
