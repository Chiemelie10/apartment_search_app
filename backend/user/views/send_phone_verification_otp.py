"""This module defines class SendEmailVerificationLink."""
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from user.verify_phone_number import send_phone_otp


User = get_user_model()

class SendPhoneVerificationOTP(APIView):
    """
    This class defines a get method that handles sending of otp to phone
    for phone number verification.
    """

    permission_classes = [IsAuthenticated]

    # Response schema for drf_spectacular
    @extend_schema(
        request=None,
        responses={
            200: {
                'example': {
                    'message': 'A One Time Password (OTP) has been sent to *********88'
                }
            }
        }
    )
    def get(self, request):
        """
        This method sends a One Time Password for phone number verification to a user's phone.\n
        Returns:\n
            On sucess: It returns a http status code of 200 with an appropriate message.\n
            On failure: An error message to the client with a corresponding http status code.
        """
        # pylint: disable=broad-exception-caught

        try:
            # Get the user object from the request.
            user = request.user

            # Check if the current phone number of the user has been already verified.
            is_verified = user.profile.phone_number_is_verified
            if is_verified is True:
                return Response(
                    {
                        'error':
                        'Phone number has already been verified.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # Send otp to the user's phone number.
            phone_number = user.profile.phone_number
            if phone_number is None:
                return Response(
                    {
                        'error':
                        'Phone number must be entered in the profile.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            send_phone_otp(phone_number)

            # Hide phone number
            if phone_number.startswith('+234'):
                hidden_phone_number = f'+234********{phone_number[-2]}{phone_number[-1]}'
            elif phone_number.startswith('234'):
                hidden_phone_number = f'234********{phone_number[-2]}{phone_number[-1]}'
            else:
                hidden_phone_number = f'*********{phone_number[-2]}{phone_number[-1]}'

            # Return a response to the client.
            return Response(
                {
                    'message':
                    f'A One Time Password (OTP) has been sent to {hidden_phone_number}.'
                },
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
