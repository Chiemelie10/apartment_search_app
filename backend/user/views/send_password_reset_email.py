"""This module defines the module ForgotPasswordView"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user.serializers import ForgotPasswordSerializer
from user.utils import send_email_verification_link


User = get_user_model()

class SendPasswordResetToken(APIView):
    """
    This class defines a post method that helps users get
    a password-reset token.
    """
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        """
        This method sends a password-reset token to a user's email address if the
        email or username in the body of the request matches any in the database.
        """
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')

            if username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            elif email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            send_email_verification_link(user, for_password=True)
            verification_token = user.verification_token

            verification_token.is_for_password_reset = True
            verification_token.is_used = False
            verification_token.is_validated_for_password_reset = False
            verification_token.otp_submission_time = None
            verification_token.save()

            message = f'A One Time Password (OTP) has been sent to {user.email}'
            return Response({'message': message}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
