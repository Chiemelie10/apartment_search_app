"""This module defines class MessageSerializer."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.utils import check_html_tags
from message.models import Message


User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    """This class defines the fields of the Message model to be validated and serialized."""
    # pylint: disable=no-member

    sender = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=True,
        queryset=User.objects.prefetch_related('sent_messages').all()
    )
    receiver = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=User.objects.prefetch_related('received_messages').all()
    )

    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = Message
        fields = ['id', 'sender', 'receiver', 'text', 'image', 'parent_message', 'created_at']

    def validate(self, attrs):
        """
        This method validates the request and returns the value of the attrs in the request.
        """
        text = attrs.get('text')
        image = attrs.get('image')

        if text is None and image is None:
            raise serializers.ValidationError('The field "text" or "image" is required.')

        return attrs

    def validate_text(self, text):
        """This method does extra validation on the text field."""
        # Check for html tags in submitted title.
        is_html_in_value, validated_value = check_html_tags(text)

        if is_html_in_value is True:
            raise serializers.ValidationError(
                'html tags or anything similar is not allowed. '\
                'Remove all angular brackets to proceed.'
            )

        return validated_value
