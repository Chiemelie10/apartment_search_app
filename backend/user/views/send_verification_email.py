"""This module defines class SendEmailVerificationLink."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user.utils import send_email_verification_link


User = get_user_model()

class SendEmailVerificationLink(APIView):
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
            send_email_verification_link(user)

            return Response({'message':
                             f'An email verification link has been sent to {user.email}'},
                             status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
