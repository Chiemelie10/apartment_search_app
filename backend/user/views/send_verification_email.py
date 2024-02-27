"""This module defines class SendEmailVerificationLink."""
from smtplib import SMTPConnectError, SMTPException
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from user.utils import send_verification_token


User = get_user_model()

class SendEmailVerificationToken(APIView):
    """This class defines a get method that handles sending verification emails."""

    permission_classes = [IsAuthenticated]

    # Response schema for drf_spectacular
    @extend_schema(
        request=None,
        responses={
            200: {
                'example': {
                    'message': 'A One Time Password (OTP) has been sent to user@example.com'
                }
            }
        }
    )
    def get(self, request, user_id):
        """
        This method sends a One Time Password for email verification to the user's email address.\n
        Args:\n
            user_id: The ID of the user.\n
        Returns:\n
            On sucess: It returns a http status code of 200 with an appropriate message.\n
            On failure: An error message to the client with a corresponding http status code.
        """
        # pylint: disable=unused-argument
        # pylint: disable=broad-exception-caught

        try:
            # Get the user object through the provided user_id in the url.
            user = User.objects.get(id=user_id)

            # Send otp to the email address provided by the user.
            send_verification_token(user)

            # Update the fields of the VerificationToken model and save.
            verification_token = user.verification_token
            verification_token.is_for_password_reset = False
            verification_token.is_used = False
            verification_token.is_validated_for_password_reset = False
            verification_token.otp_submission_time = None
            verification_token.save()

            # Return a response to the client.
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
