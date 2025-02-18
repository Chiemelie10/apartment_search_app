"""This module defines class GetUserMessagesView."""
from django.db.models import Subquery, OuterRef, Q
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

class GetUserMessagesView(APIView):
    """
    This class defines methods that gets a user's messages from the database.
    """
    #pylint: disable=no-member
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    @extend_schema(
        request=None
    )
    def get(self, request, user_id):
        """
        For the user making the request, this method gets only the last message
        the user sent or received from each user that contacted the user previously.
        """
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
            url_name='get_user_messages',
            arg1=user_id
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
