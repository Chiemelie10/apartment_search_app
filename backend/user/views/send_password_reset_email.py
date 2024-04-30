"""This module defines the module ForgotPasswordView"""
from smtplib import SMTPConnectError, SMTPException
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from user.serializers import SendPasswordResetTokenSerializer
from user.utils import send_verification_token


User = get_user_model()

class SendPasswordResetToken(APIView):
    """
    This class defines a post method that helps users get
    a password-reset token.
    """
    serializer_class = SendPasswordResetTokenSerializer

    def get_request_user(self, validated_data):
        """
        Args:
            validated_data: The data in the body of the request validated
            by the ForgotPasswordSerializer.
        Returns:
            On success: This method identifies if username or email was
            submitted by the user and returns the user object.
            On failure: None
        """
        username = validated_data.get('username')
        email = validated_data.get('email')

        # Get user object that will be passed into the send_verification_token function.
        if username:
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                return None
        elif email:
            try:
                user = User.objects.get(email=email)
                return user
            except User.DoesNotExist:
                return None

    # Response schema for drf_spectacular
    @extend_schema(
        responses={
            200: {
                'example': {
                    'message': 'A One Time Password (OTP) has been sent to user@example.com'
                }
            }
        }
    )
    def post(self, request):
        """
        This method sends a password-reset token to a user's email address if the
        email or username in the body of the request matches any in the database.\n
        Returns:\n
            On success: It returns a http status code of 200 with an appropriate message.\n
            On failure: It returns an error message with a corresponding http status code.
        """
        # pylint: disable=broad-exception-caught

        # Validate data in request body and return error messages if exception is raised.
        serializer = SendPasswordResetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get user object that will be passed into the send_verification_token function.
        user = self.get_request_user(serializer.validated_data)
        if user is None:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Send otp for password reset to the user's email
            send_verification_token(user, for_password=True)

            # Update the fields of the VerificationToken model and save
            verification_token = user.verification_token
            verification_token.is_for_password_reset = True
            verification_token.is_used = False
            verification_token.is_validated_for_password_reset = False
            verification_token.otp_submission_time = None
            verification_token.save()

            # Return response to the client if email was sent successfully.
            message = f'A One Time Password (OTP) has been sent to {user.email}.'
            return Response({'message': message}, status=status.HTTP_200_OK)
        except SMTPConnectError:
            return Response({'error': 'Failed to send email due to connection issues.'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except SMTPException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
