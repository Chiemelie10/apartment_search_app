"""This module defines class SendEmailVerificationLink."""
from smtplib import SMTPConnectError, SMTPException
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user.utils import send_verification_token


User = get_user_model()

class SendEmailVerificationToken(APIView):
    """This class defines a get method that handles sending verification emails."""
    def get(self, request, user_id):
        """
            args:
                - user_id: The ID of the user
            returns:
                - On sucess: An email verification link to the user's email address.
                - On failure: An error message to the client that made the request.
        """
        # pylint: disable=unused-argument
        # pylint: disable=broad-exception-caught

        try:
            user = User.objects.get(id=user_id)
            send_verification_token(user)

            verification_token = user.verification_token

            verification_token.is_for_password_reset = False
            verification_token.is_used = False
            verification_token.is_validated_for_password_reset = False
            verification_token.otp_submission_time = None
            verification_token.save()

            return Response({'message':
                             f'A One Time Password (OTP) has been sent to {user.email}.'},
                             status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except SMTPConnectError:
            return Response({'error': 'Failed to send email due to connection issues.'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except SMTPException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
