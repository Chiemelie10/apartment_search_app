"""This module defines class GetUserToUserMessages."""
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from message.serializers import MessageSerializer
from message.models import Message
from apartment.utils import (
    get_page_and_size,
    get_prev_and_next_page,
    paginate_queryset
)


User = get_user_model()

class GetUserToUserMessages(APIView):
    """
    This class defines methods that gets all messages between two users.
    """
    #pylint: disable=no-member
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    @extend_schema(
        request=None
    )
    def get(self, request, user_id, user2_id):
        """
        This method gets all messages for the owner of the account
        (user) had with another user (user2).
        """
        user = request.user

        # Confirm the id of the user making the request is equal to user_id
        # Return an error response if it is not equal.
        if user.id != user_id:
            return Response(
                {
                    'error': 'This user is not permitted to access this resource.'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Get messages between the owner of the account and another user
        messages = Message.objects.filter(
            Q(sender=user_id, receiver=user2_id) |
            Q(sender=user2_id, receiver=user_id)
        ).order_by('-created_at')

        # Get the values of page and page_size from query string of the request.
        try:
            page, page_size = get_page_and_size(request)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # Return the messages without pagination if page and page size were not provided.
        if page is None and page_size is None:
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Get paginated queryset from the messages queryset
        try:
            paginated_data, total_pages = paginate_queryset(messages, page, page_size)
        except ValueError as exc:
            if str(exc).lower() == 'page not found.':
                return Response({'error': str(exc)}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize paginated queyset.
        serializer = MessageSerializer(paginated_data, many=True)

        # Get values of previous and next pages.
        previous_page, next_page = get_prev_and_next_page(
            request,
            page,
            page_size,
            total_pages,
            url_name='get_user_to_user_messages',
            arg1=user_id,
            arg2=user2_id
        )

        data = {
            'total_number_of_messages': len(messages),
            'total_pages': total_pages,
            'previous_page': previous_page,
            'current_page': page,
            'next_page': next_page,
            'messages': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
