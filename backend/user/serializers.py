"""This module defines class UserSerializer."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from user_verification_token.models import VerificationToken
from user.models import UserProfile, UserProfileInterest
from user.utils import check_html_tags, resize_image
from user_suspension.models import UserSuspension
from user_interest.models import UserInterest
from user_interest.serializers import UserInterestSerializer


User = get_user_model()

class UserProfileInterestSerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the UserProfileInterest model
    to be validated when a request is made.
    """
    # pylint: disable=no-member
    user_profile = serializers.PrimaryKeyRelatedField(read_only=True)
    user_interest = UserInterestSerializer(required=True)
    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the name model to be validated or serialized.
        """
        model = UserProfileInterest
        fields = ['id', 'user_profile', 'user_interest']

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
    phone_number = serializers.CharField(required=True, allow_null=True)
    gender = serializers.CharField(required=True, allow_null=True)
    first_name = serializers.CharField(required=True, allow_null=True)
    last_name = serializers.CharField(required=True, allow_null=True)
    thumbnail=serializers.ImageField(required=True, allow_null=True)
    remove_thumbnail = serializers.BooleanField(default=False)
    email=serializers.EmailField(required=False)

    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = UserProfile
        fields = [
            'gender',
            'phone_number',
            'phone_number_is_verified',
            'interests',
            'thumbnail',
            'remove_thumbnail',
            'first_name',
            'last_name',
            'email',
        ]

    def validate(self, attrs):
        """
        This method does extra validation on one or more fields of the
        UserProfile model.
        """
        thumbnail = attrs.get('thumbnail')
        remove_thumbnail = attrs.get('remove_thumbnail', False)

        if thumbnail is not None and remove_thumbnail is True:
            raise serializers.ValidationError(
                'The field "remove_thumbnail" cannot be false when thumbnail is not null.'
            )

        return attrs

    def validate_email(self, email):
        """This method does extra validation on the role field."""
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError('User with the email already exists.')
        except User.DoesNotExist:
            return email

    def validate_interests(self, interests):
        """This method does extra validation on the interests field."""
        if interests is None:
            interests = []

        for interest in interests:
            value = interest.get('user_interest')
            if value.name.lower() == 'none':
                if len(interests) > 1:
                    raise serializers.ValidationError(
                        'There cannot be more than one interest when "none" is entered.'
                    )

        # Add none to list of interests if empty list was submitted.
        if interests == []:
            user_interest = UserInterest.objects.get(name='None')
            interests.append({'user_interest': user_interest})

        return interests


    def validate_phone_number(self, phone_number):
        """This method does extra validation on the phone_number field."""
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
        if first_name is None:
            return first_name

        is_html_in_value, validated_value = check_html_tags(first_name)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

        return validated_value

    def validate_last_name(self, last_name):
        """This method does extra validation on the last name field."""
        if last_name is None:
            return None

        is_html_in_value, validated_value = check_html_tags(last_name)

        if is_html_in_value is True:
            raise serializers.ValidationError('html tags or anything similar is not allowed.')

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
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password is required.'
        }
    )
    username = serializers.CharField(
        error_messages={
            'required': 'Username is required.',
            'blank': 'Username is required.',
        }
    )
    email = serializers.EmailField(
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email is required.'
        }
    )
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
        fields = [
            'id', 'username', 'email', 'password', 'profile_information',
            'is_active', 'is_staff', 'is_superuser', 'is_verified',
            'created_at', 'updated_at'
        ]

    def to_representation(self, instance):
        """
        This method is overridden to define data that is returned when
        object is serialized using the UserSerializer.
        """
        data = super().to_representation(instance)
        data['profile_information'].pop('remove_thumbnail')

        # Check if current user is the owner of the profile
        user = self.context['request'].user
        method = self.context['request'].method

        if user != instance and user.is_staff is False and method != 'POST':
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
                'phone_number_is_verified',
                'first_name',
                'last_name'
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
        try:
            validate_password(value)
        except ValidationError as e:
            raise e

        return value

    def validate_username(self, value):
        """This method does extra validation on the username field."""
        is_html_in_value, validated_value = check_html_tags(value)

        if is_html_in_value is True:
            raise serializers.ValidationError(
                'Angle brackets are not allowed. Please remove it to proceed.'
            )

        if User.objects.filter(username=validated_value).exists():
            raise serializers.ValidationError(
                'This username has been taken. Please use a different username.'
            )

        return validated_value

    def validate_email(self, value):
        """This method does extra validation on the email field."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'This email has been taken. Please use a different email address.'
            )

        return value


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
class SendPasswordResetTokenSerializer(serializers.Serializer):
    """
    This class validates the fields of a POST request
    made to the change password endpoint.
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
    username = serializers.CharField(
        write_only=True,
        required=False,
        error_messages={
            'required': 'Username is required.',
            'blank': 'Username is required.'
        }
    )
    email = serializers.EmailField(
        write_only=True,
        required=False,
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email is required.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password is required.'
        }
    )
    username_or_email = serializers.CharField(
        write_only=True,
        required=False,
        error_messages={
            'required': 'Username or email is required.',
            'blank': 'Username or email is required.'
        }
    )

    def validate(self, attrs):
        """
        This method validates the request and returns the
        value of the attrs in the request.
        """
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        username_or_email = attrs.get('username_or_email')

        if not email and not username and not username_or_email:
            raise serializers.ValidationError('Email or username is required.')

        if email and username:
            raise serializers.ValidationError('Provide either email or username, not both.')

        if email and username_or_email:
            raise serializers.ValidationError('Provide either email or username, not both.')

        if username and username_or_email:
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
    

class ValidatePhoneOTPSerializer(serializers.Serializer):
    """
    This class validates the fields of a POST request
    made to the endpoint that validates the otp provided
    by a user from their phone.
    """
    otp = serializers.CharField(write_only=True, required=True)

    def validate_otp(self, otp):
        """
        This method validates the otp provided by the user.
        """
        if len(otp) > 6:
            raise serializers.ValidationError('The One Time Password entered is incorrect.')

        return otp
