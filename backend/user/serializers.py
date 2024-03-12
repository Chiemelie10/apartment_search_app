"""This module defines class UserSerializer."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from user_verification_token.models import VerificationToken
from user.models import UserProfile, UserProfileInterest
from user.utils import check_html_tags, resize_image
from user_interest.models import UserInterest
from user_role.models import UserRole


User = get_user_model()

class UserProfileInterestSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the UserProfileInterest model
    to be validated when a request is made.
    """
    # pylint: disable=no-member
    user_profile = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = UserProfileInterest
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the UserProfile model
    to be validated when a request is made.
    """
    # pylint: disable=no-member
    interests = UserProfileInterestSerializer(
            required=False, many=True, source='userprofileinterest_set'
    )
    role = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=UserRole.objects.prefetch_related('profiles').all()
    )
    phone_number = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = UserProfile
        fields = [
            'role',
            'gender',
            'phone_number',
            'interests',
            'thumbnail',
            'first_name',
            'last_name'
        ]

    def validate_interests(self, interests):
        """This method does extra validation on the phone_number field."""
        # pylint: disable=no-member

        if len(interests) > 0:
            validated_interests = []
            for interest in interests:
                user_interest = interest['user_interest']
                try:
                    user_interest = UserInterest.objects.get(pk=user_interest.id)
                    validated_interests.append(user_interest)
                except UserInterest.DoesNotExist as error:
                    raise error
        return validated_interests

    def validate_phone_number(self, phone_number):
        """This method does extra validation on the phone_number field."""
        if phone_number is None or phone_number == '':
            raise serializers.ValidationError('Phone number is required.')

        # Check for html tags in submitted phone number.
        is_html_in_value, validated_value = check_html_tags(phone_number)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

        if len(validated_value) < 11 or len(validated_value) == 12 or len(validated_value) > 14:
            raise serializers.ValidationError(
                'The number of digits for the phone number entered '\
                'cannot less than 11, exactly 12, or greater than 14.'
            )

        # Validate phone numbers that start with +
        new_value = None

        if validated_value.startswith('+'):
            new_value = validated_value.replace('+', '', 1)
            if len(new_value) != 13 or new_value.startswith('234') is False:
                raise serializers.ValidationError(
                    'The country code for Nigeria phone numbers must be used.'
                )
            if new_value.isdigit() is False:
                raise serializers.ValidationError(
                    'Only numbers must follow the "+" sign.'
                )

        if new_value:
            accepted_value = new_value.replace('234', '+234', 1)
            return accepted_value

        # Validate phone numbers without plus
        if validated_value.isdigit() is False:
            raise serializers.ValidationError(
                'Only numbers can be used.'
            )

        if len(validated_value) != 11 and len(validated_value) != 13:
            raise serializers.ValidationError(
                'The number of digits for the phone number entered must be exactly 11 or 13.'
            )

        if len(validated_value) == 11 and validated_value.startswith('0') is False:
            raise serializers.ValidationError(
                'The phone number must start with "0" when the number '\
                'of digits for the phone number is 11.'
            )

        if len(validated_value) == 13 and validated_value.startswith('234') is False:
            raise serializers.ValidationError(
                'The phone number must start with "234" when the number '\
                'of digits for the phone number is 13.'
            )

        if len(validated_value) == 11:
            accepted_value = validated_value.replace('0', '+234', 1)
        elif len(validated_value) == 13:
            accepted_value = validated_value.replace('234', '+234', 1)

        return accepted_value

    def validate_first_name(self, first_name):
        """This method does extra validation on the first name field."""
        is_html_in_value, validated_value = check_html_tags(first_name)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

        if len(validated_value) > 250:
            raise serializers.ValidationError(
                'Ensure first name has no more than 250 characters.'
            )

        return validated_value

    def validate_last_name(self, last_name):
        """This method does extra validation on the last name field."""
        is_html_in_value, validated_value = check_html_tags(last_name)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

        if len(validated_value) > 250:
            raise serializers.ValidationError(
                'Ensure last name has no more than 250 characters.'
            )

        return validated_value

    def validate_thumbnail(self, thumbnail):
        """This method does extra validation on the last name field."""
        if thumbnail is None:
            return None

        allowed_mimetypes = ['image/jpeg']

        if thumbnail.content_type not in allowed_mimetypes:
            raise serializers.ValidationError('Invalid mime type. Only image/jpeg can be used.')

        resized_thumbnail = resize_image(image=thumbnail, new_width=300)

        return resized_thumbnail


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
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

        try:
            validate_password(validated_value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return validated_value

    def validate_username(self, value):
        """This method does extra validation on the username field."""
        is_html_in_value, validated_value = check_html_tags(value)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

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

    def validate_password(self, value):
        """This method does extra validation on the password field."""
        is_html_in_value, validated_value = check_html_tags(value)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

        try:
            validate_password(validated_value)
        except ValidationError as e:
            raise e

        return validated_value

class LoginSerializer(serializers.Serializer):
    """
    This class lists the User class attributes that will be
    validated in the LoginView.
    """
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """
        This method validates the request and returns the
        value of the attrs in the request.
        """
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not email and not username:
            raise serializers.ValidationError('Email or username is required.')

        if email and username:
            raise serializers.ValidationError('Provide either email or username, not both.')

        if not password:
            raise serializers.ValidationError('Password is required.')

        return attrs
