"""This module defines class UserSerializer."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from user_verification_token.models import VerificationToken
from user.models import UserProfile, UserProfileInterest
from user.utils import check_html_tags, resize_image
from user_role.models import UserRole
from user_suspension.models import UserSuspension


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
            fields: The class attributes of the name model to be validated or serialized.
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
            required=True,
            many=True,
            source='userprofileinterest_set'
    )
    role = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=True,
        queryset=UserRole.objects.prefetch_related('profiles').all()
    )
    phone_number = serializers.CharField(required=True, allow_null=True)
    gender = serializers.CharField(required=True, allow_null=True)
    first_name = serializers.CharField(required=True, allow_null=True)
    last_name = serializers.CharField(required=True, allow_null=True)
    thumbnail=serializers.ImageField(required=True, allow_null=True)
    email=serializers.EmailField(required=False)

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
            'last_name',
            'email',
        ]
    def validate_email(self, email):
        """This method does extra validation on the role field."""
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError('User with the email already exists.')
        except User.DoesNotExist:
            return email

    def validate_role(self, role):
        """This method does extra validation on the role field."""
        request_method = self.context['request'].method

        if request_method == 'PUT':
            if role is None or role == '':
                raise serializers.ValidationError('The field "role" is required.')

        return role

    def validate_gender(self, gender):
        """This method does extra validation on the role field."""
        request_method = self.context['request'].method

        if request_method == 'PUT':
            if gender is None or gender == '':
                raise serializers.ValidationError('The field "gender" is required.')

        return gender

    def validate_interests(self, interests):
        """This method converts interests from a list of dictionary to a list."""
        if len(interests) > 0:
            validated_interests = []
            for interest in interests:
                user_interest = interest['user_interest']
                validated_interests.append(user_interest)
        return validated_interests

    def validate_phone_number(self, phone_number):
        """This method does extra validation on the phone_number field."""
        request_method = self.context['request'].method

        if request_method == 'PUT':
            if phone_number is None or phone_number == '':
                raise serializers.ValidationError('The field "phone_number" is required.')

        if phone_number is None:
            return None

        # Check for html tags in submitted phone number.
        is_html_in_value, validated_value = check_html_tags(phone_number)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

        if validated_value.isdigit() is False:
            raise serializers.ValidationError(
                'Only numbers must be used.'
            )

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
        request_method = self.context['request'].method

        if request_method == 'PUT':
            if first_name is None or first_name == '':
                raise serializers.ValidationError('The field "first_name" is required.')

        if first_name is None:
            return first_name

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
        request_method = self.context['request'].method

        if request_method == 'PUT':
            if last_name is None or last_name == '':
                raise serializers.ValidationError('The field "last_name" is required.')

        if last_name is None:
            return None

        is_html_in_value, validated_value = check_html_tags(last_name)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

        if len(validated_value) > 250:
            raise serializers.ValidationError(
                'Ensure last name has no more than 250 characters.'
            )

        return validated_value

    def validate_thumbnail(self, thumbnail):
        """This method does extra validation on the thumbnail field."""
        if thumbnail is None:
            return thumbnail

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

    def to_representation(self, instance):
        """
        This method is overridden to define data that is returned when
        object is serialized using the UserSerializer.
        """
        data = super().to_representation(instance)

        # Check if current user is the owner of the profile
        user = self.context['request'].user
        if user != instance and user.is_staff is False and user.is_authenticated is True:
            excluded_fields = [
                'email',
                'id',
                'is_superuser',
                'is_staff',
                'is_active',
                'is_verified',
                'created_at',
                'updated_at',
                'last_login',
                'groups',
                'user_permissions',
                'phone_number',
                'first_name',
                'last_name',
                'role'
            ]
            for field in excluded_fields:
                if field in (
                    'id', 'email', 'is_superuser', 'is_staff',
                    'is_active', 'is_verified', 'created_at',
                    'updated_at', 'last_login', 'groups', 'user_permissions'
                ):
                    data.pop(field, None)
                else:
                    data['profile_information'].pop(field, None)

        return data

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


class TokenBlacklistSerializer(serializers.ModelSerializer):
    """
    This class lists the class attributes that will be
    validated in the TokenBlacklistView.
    """
    # user = serializers.CharField(required=True)
    # duration = serializers.IntegerField(default=None, allow_null=True)
    # is_permanent = serializers.BooleanField(default=False)
    # has_ended = serializers.BooleanField(default=False)

    user = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=User.objects.all()
    )
    is_permanent = serializers.BooleanField(required=False)
    has_ended = serializers.BooleanField(required=False)
    duration = serializers.IntegerField(required=True, allow_null=True)

    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = UserSuspension
        fields = ['user', 'is_permanent', 'duration', 'has_ended']

    def to_representation(self, instance):
        """
        This method is overridden to define data that is returned when
        object is serialized using the TokenBlacklistSerializer.
        """
        data = super().to_representation(instance)
        data['start_time'] = instance.start_time
        data['end_time'] = instance.end_time
        data['number_of_suspensions'] = instance.number_of_suspensions
        return data

    def validate(self, attrs):
        """
        This method validates the request and returns the
        value of the attrs in the request.
        """
        # Get request method
        method = self.context['request'].method

        is_permanent = attrs.get('is_permanent')
        duration = attrs.get('duration')
        has_ended = attrs.get('has_ended')

        if method == 'POST' and has_ended is True:
            raise serializers.ValidationError(
                'The "has_ended" field should not be set to true in a post request. '\
                'Remove it from the request or set it to false.'
            )

        if 'user' not in attrs.keys():
            raise serializers.ValidationError('The field "user" is required.')

        if has_ended is True:
            if 'is_permanent' in attrs.keys() or 'duration' in attrs.keys():
                raise serializers.ValidationError(
                    'The field "is_permanent" and/or "duration" should not be included '\
                    'in the request body when the field "has_ended" is set to true.'
                )

        if is_permanent is False and duration is None:
            raise serializers.ValidationError(
                'The field "duration" is required when is_permanent is False.'
            )

        if is_permanent is True and duration is not None:
            raise serializers.ValidationError(
                'The field "duration" should not be set when is_permanent is True.'
            )

        if has_ended is True and duration is not None:
            return serializers.ValidationError(
                'The "has_ended" field should not be set to true when the field "duration" '\
                'is set. Remove it from the request or set it to false.'
            )

        if has_ended is True and is_permanent is True:
            return serializers.ValidationError(
                'The "has_ended" field should not be set to true when the field "is_permanent" '\
                'is also set to True. Remove it from the request or set it to false.'
            )

        if duration is not None:
            if duration < 1:
                raise serializers.ValidationError('Duration cannot be less than one hour.')

            if (duration % 1) != 0:
                raise serializers.ValidationError('Duration must be a whole number.')

        return attrs
