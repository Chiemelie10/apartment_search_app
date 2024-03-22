"""This module defines class UserView"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from user.serializers import UserSerializer


User = get_user_model()

class UserView(APIView):
    """This class defines a method that gets, update or delete a user's data."""

    # serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserSerializer}
    )
    def get(self, request):
        """
        This method returns all users that registered on the application.\n
        Returns:\n
            On success: Http status code of 200 and the data of each user.\n
            On failure: Appropriate http status code and error message.
        """
        if request.user.is_staff is False:
            return Response(
                {
                    'error': 'This user has no permission to '\
                        'access the requested resource.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
