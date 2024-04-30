"""This module defines class ApartmentSearch"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apartment.models import Apartment
from apartment.serializers import ApartmentSerializer, ApartmentSearchSerializer
from apartment.utils import (
    paginate_queryset,
    get_page_and_size,
    get_prev_and_next_page
)


class ApartmentSearchView(APIView):
    """
    This module defines a method that returns apartment(s) depending on the
    values of the query string parameters gotten from the url of the request.
    """
    serializer_class = ApartmentSearchSerializer

    @extend_schema(
        responses={200: ApartmentSerializer}
    )
    def post(self, request):
        """
        This method returns apartments that matches the search query
        entered by the user.
        """
        # pylint: disable=no-member

        serializer = ApartmentSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        country = validated_data.get('country')
        state = validated_data.get('state')
        city = validated_data.get('city')
        school = validated_data.get('school')
        listing_type = validated_data.get('listing_type')
        max_price = validated_data.get('max_price')
        min_price = validated_data.get('min_price')
        amenities = validated_data.get('apartmentamenity_set')

        apartments = Apartment.objects.all()

        if country is not None:
            apartments = apartments.filter(country=country)

        if state is not None:
            apartments = apartments.filter(state=state)

        if city is not None:
            apartments = apartments.filter(city=city)

        if school is not None:
            apartments = apartments.filter(school=school)

        if listing_type is not None:
            apartments = apartments.filter(listing_type=listing_type)

        if min_price is not None and max_price is not None:
            apartments = apartments.filter(price__range=(min_price, max_price))
        elif min_price is None and max_price is not None:
            apartments = apartments.filter(price__range=(0, max_price))

        if amenities is not None:
            for amenity in amenities:
                amenity_obj = amenity.get('amenity')
                amenity_quantity = amenity.get('quantity')
                if amenity is not None:
                    try:
                        if amenity_quantity is not None:
                            amenity_quantity = int(amenity_quantity)
                            apartments = apartments.filter(
                                amenities__id=amenity_obj.id,
                                apartmentamenity__quantity=amenity_quantity
                            )
                        else:
                            apartments = apartments.filter(amenities__id=amenity_obj.id)
                    except ValueError:
                        return Response(
                            {'error': 'The value for "amenity" and "quantity" must be numbers.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

        # Order the apartments queryset by inverse of created_at
        apartments = apartments.order_by('-created_at')

        # Get the values of page and page_size from query string of the request.
        try:
            page, page_size = get_page_and_size(request)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

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
            url_name='search_apartments'
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
