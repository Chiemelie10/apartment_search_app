"""This module defines class GetApartmentsView."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apartment.models import Apartment
from apartment.utils import (
    get_page_and_size,
    get_prev_and_next_page,
    paginate_queryset
)
from apartment.serializers import ApartmentSerializer


class GetApartmentsView(APIView):
    """This class defines methods that gets, updates or deletes an apartment object."""

    permission_classes = [IsAuthenticated]
    serializer_class = ApartmentSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page',
                location=OpenApiParameter.QUERY,
                description='Page number',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='size',
                location=OpenApiParameter.QUERY,
                description='Number of items per page',
                required=False,
                type=int
            )
        ]
    )
    def get(self, request):
        """
        This method gets all apartment adverts in the database.\n
        Returns:\n
            On success: A http status code of 200 and data of the apartments.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member

        # Allow access to only users that are staff
        if request.user.is_staff is False:
            return Response(
                {'error': 'This user is not permitted to access this resource.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the values of page and page_size from query string of the request.
        try:
            page, page_size = get_page_and_size(request)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # Get all apartments
        apartments = Apartment.objects.all().order_by('-created_at')

        # Return all apartments without pagination if page and page size were not provided.
        if page is None and page_size is None:
            serializer = ApartmentSerializer(apartments, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Get paginated queryset from the apartments queryset
        try:
            paginated_data, total_pages = paginate_queryset(apartments, page, page_size)
        except ValueError as exc:
            if str(exc).lower() == 'page not found.':
                return Response({'error': str(exc)}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # serialize paginated queyset.
        serializer = ApartmentSerializer(paginated_data, many=True, context={'request': request})

        # Get values of previous and next pages.
        previous_page, next_page = get_prev_and_next_page(
            request,
            page,
            page_size,
            total_pages,
            url_name='get_apartments'
        )

        data = {
            'total_number_of_apartments': len(apartments),
            'total_pages': total_pages,
            'previous_page': previous_page,
            'current_page': page,
            'next_page': next_page,
            'apartments': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
