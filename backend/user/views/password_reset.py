"""This module defines class PasswordResetView."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import PasswordResetSerializer
from user.utils import is_otp_submission_time_expired
from user_verification_token.models import VerificationToken


class PasswordResetView(APIView):
    """
    This class defines a method that resets a user's
    password in the database.
    """

    serializer_class = PasswordResetSerializer

    def post(self, request):
        """
        This resets a user's password in the data base.
            On success: It returns a 200 Ok http status code.
            On failure: It returns an appropriate error message and status code.
        """
        # pylint: disable=no-member

        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            verification_token = serializer.validated_data.get('verification_token')
            password = serializer.validated_data.get('password')

            try:
                token = VerificationToken.objects.get(verification_token=verification_token)

                if token.is_for_password_reset is False or token.is_validated_for_password_reset is False:
                    return Response({'error': 'You are not permitted to use this resource.'},
                                    status=status.HTTP_401_UNAUTHORIZED)

                if token.is_used is True:
                    return Response({'error': 'Token has been used'},
                                    status=status.HTTP_400_BAD_REQUEST)

                token_expired = is_otp_submission_time_expired(token, 600)
                if token_expired is True:
                    return Response({'error': 'Token submission time has elapsed.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                user = token.user
                user.set_password(password)
                user.save()

                token.is_used = True
                token.save()

                message = 'Password reset was successful.'
                return Response({'message': message}, status=status.HTTP_200_OK)
            except VerificationToken.DoesNotExist:
                return Response({'error': 'Token is incorrect'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
