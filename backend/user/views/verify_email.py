"""This module defines class ActivateAccount."""
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user.serializers import VerifyEmailSerializer
from user.utils import is_token_expired


load_dotenv()
User = get_user_model()

class VerifyEmail(APIView):
    """This class defines a method that handles activation of account."""

    serializer_class = VerifyEmailSerializer

    def post(self, request, user_id):
        """
        This method sets the is_verified field of the User model to true.

        returns:
            - On sucess: A success message to the client.
            - On failure: The reason for the failure to the client.
        """
        # pylint: disable=no-member

        serializer = VerifyEmailSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            verification_token = validated_data.get('verification_token')

            try:
                user = User.objects.get(id=user_id)
                token = user.verification_token

                if user.is_verified is True:
                    return Response({'error': 'Account has already been verified.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if verification_token != token.verification_token:
                    return Response({'error': 'Token is incorrect'},
                                    status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            token_expired = is_token_expired(token, 600)

            if token_expired is True:
                return Response({'error': 'Token has expired'},
                                status=status.HTTP_400_BAD_REQUEST)

            user.is_verified = True
            user.save()

            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
