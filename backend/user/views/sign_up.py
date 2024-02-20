"""This module defines the CreateUserView."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer


User = get_user_model()

class SignUpView(APIView):
    """This class defines methods that handles CRUD operations relating to the User model"""
    serializer_class = UserSerializer

    def crosscheck_validated_data(self, validated_data):
        """
        This method ensures a superuser and staff accounts can't be created through this view.
        It also ensures emails are not authomatically verified on creating new
        student or agent accounts.
        """
        is_superuser = validated_data.get('is_superuser')
        is_staff = validated_data.get('is_staff')
        is_verified = validated_data.get('is_verified')
        is_active = validated_data.get('is_active')

        if is_superuser is True:
            validated_data['is_superuser'] = False
        if is_staff is True:
            validated_data['is_staff'] = False
        if is_verified is True:
            validated_data['is_verified'] = False
        if is_active is False:
            validated_data['is_active'] = True

    def post(self, request):
        """This method creates a new user instance and saves it to the database."""
        if request.content_type != 'application/json':
            return Response({'error': 'Content-Type must be application/json.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            self.crosscheck_validated_data(validated_data)
            password = validated_data.pop('password')
            email = validated_data.pop('email')
            username = validated_data.pop('username')

            user = User.objects.create_user(password=password, email=email,
                                            username=username, **validated_data)

            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
