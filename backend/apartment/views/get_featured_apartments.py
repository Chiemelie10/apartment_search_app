"""This module defines class FeaturedApartmentsView"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.utils import timezone
from apartment.models import Apartment
from apartment.serializers import ApartmentSerializer
from apartment.utils import (
    get_page_and_size,
    get_prev_and_next_page,
    paginate_queryset
)


class FeaturedApartmentsView(APIView):
    """
    This class defines a method gets all apartment objects that have
    is_featured property set to true and is_taken property set to false.
    """

    serializer_class = ApartmentSerializer

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
        This method gets all apartment objects that have is_featured property set to true
        and is_taken property set to false.\n
        Returns:\n
            On success: A http status code of 200 and data of the featured apartments.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member

        # Get the values of page and page_size from query string of the request.
        try:
            page, page_size = get_page_and_size(request)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # Get all apartments
        featured_apartments = Apartment.objects.filter(
            is_featured=True,
            is_taken=False,
            approval_status='accepted',
            advert_exp_time__gt=timezone.now()
        ).order_by('-created_at')

        # Return all featured apartments without pagination if page
        # and page size were not provided.
        if page is None and page_size is None:
            serializer = ApartmentSerializer(
                featured_apartments, many=True, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Get paginated queryset from the apartments queryset
        try:
            paginated_data, total_pages = paginate_queryset(
                featured_apartments, page, page_size
            )
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
            url_name='featured_apartments'
        )

        data = {
            'total_number_of_apartments': len(featured_apartments),
            'total_pages': total_pages,
            'previous_page': previous_page,
            'current_page': page,
            'next_page': next_page,
            'apartments': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
