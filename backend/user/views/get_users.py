"""This module defines class UserView"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from user.serializers import UserSerializer


User = get_user_model()

class UserView(APIView):
    """This class defines a method that gets, update or delete a user's data."""

    # serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

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
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
