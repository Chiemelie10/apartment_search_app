"""This module defines class GetUserMessagesView."""
from django.db.models import Subquery, OuterRef, Q
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from message.serializers import MessageSerializer
from message.models import Message


User = get_user_model()

class GetUserMessagesView(APIView):
    """
    This class defines methods that gets, updates and deletes
    messages from the database.
    """
    #pylint: disable=no-member
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, user_id):
        """This method gets all messages sent and received by a user."""

        user = request.user
        if user.id != user_id:
            return Response(
                {
                    'error': 'This user is not permitted to access this resource.'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        messages = Message.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sent_messages__receiver=user_id) | Q(received_messages__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        Message.objects.filter(
                            Q(sender=OuterRef('id'), receiver=user_id) |
                            Q(receiver=OuterRef('id'), sender=user_id)
                        ).order_by('-created_at').values_list('id', flat=True)[:1]
                    )
                ).values_list('last_msg', flat=True).order_by('-created_at')
            )
        ).order_by('-created_at')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
