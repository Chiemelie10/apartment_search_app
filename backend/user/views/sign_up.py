"""This module defines the CreateUserView."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from user.serializers import UserSerializer


User = get_user_model()

class SignUpView(APIView):
    """This class defines methods that handles user sign up."""
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

    @extend_schema(
        responses={201: UserSerializer}
    )
    def post(self, request):
        """
        This method is used to register new users.\n
        Returns:\n
            On success: It returns a http status code of 200 with the user's newly created data.\n
            On failure: It returns an error message with a corresponding http status code.
        """
        # pylint: disable=no-member

        # Enforce the Content-Type of the request to be in application/json format.
        if request.content_type != 'application/json':
            return Response({'error': 'Content-Type must be application/json.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate data in request body and return error messages if exception is raised.
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform further validation checks on  validated data.
        validated_data = serializer.validated_data
        self.crosscheck_validated_data(validated_data)

        # Remove and take note of the values for password, email and username.
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')

        # Create the user and save to the database.
        user = User.objects.create_user(password=password, email=email,
                                        username=username, **validated_data)

        # Serialize the data of the user
        serializer = UserSerializer(user, context={'request': request})

        # Return a response to the client.
        return Response(serializer.data, status=status.HTTP_201_CREATED)
