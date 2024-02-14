"""This module defines class UserSerializer."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from user_verification_token.models import VerificationToken
from user.models import UserProfile
from user.utils import check_html_tags


User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the UserProfile model
    to be validated when a request is made.
    """
    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the User model to
    be validated when a request to register a user is made.
    """
    password = serializers.CharField(write_only=True)
    profile_information = UserProfileSerializer(
        source='profile', read_only=True, required=False
    )

    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = User
        fields = '__all__'

    def validate_password(self, value):
        """This method does extra validation on the password field."""
        is_html_in_value, validated_value = check_html_tags(value)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed')

        try:
            validate_password(validated_value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return validated_value

    def validate_username(self, value):
        """This method does extra validation on the username field."""
        is_html_in_value, validated_value = check_html_tags(value)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed')

        return validated_value


class VerificationTokenSerializer(serializers.ModelSerializer):
    """This defines attributes of the VerificationModel that will be validated"""
    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = VerificationToken
        fields = ['verification_token']


# pylint: disable=abstract-method
class ForgotPasswordSerializer(serializers.Serializer):
    """
    This class validates the fields of a POST request
    made to the forgot password endpoint.
    """
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    def validate(self, attrs):
        """
        This method validates the request and returns the
        value of the attrs in the request.
        """
        email = attrs.get('email')
        username = attrs.get('username')

        if not email and not username:
            raise serializers.ValidationError('Email or username is required.')

        if email and username:
            raise serializers.ValidationError('Provide either email or username, not both.')

        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """
    This class validates the fields of a POST request
    made to the password reset endpoint.
    """
    password = serializers.CharField(write_only=True)
    verification_token = serializers.CharField(write_only=True)

    def validate_password(self, value):
        """This method does extra validation on the password field."""
        is_html_in_value, validated_value = check_html_tags(value)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed')

        try:
            validate_password(validated_value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return validated_value
