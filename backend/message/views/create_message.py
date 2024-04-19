"""This module defines class CreateMessageView."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from message.serializers import MessageSerializer
from message.models import Message


class CreateMessageView(APIView):
    """
    This class defines a method that creates and saves messages from
    one user to another in the database.
    """
    #pylint: disable=no-member
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    @extend_schema(
        responses={201: MessageSerializer}
    )
    def post(self, request):
        """This method creates and saves messages to the database."""

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        receiver = validated_data.get('receiver')
        text = validated_data.get('text')
        image = validated_data.get('image')
        parent_message = validated_data.get('parent_message')

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            text=text,
            image=image,
            parent_message=parent_message
        )

        serializer = MessageSerializer(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
