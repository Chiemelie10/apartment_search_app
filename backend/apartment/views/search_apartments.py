"""This module defines class ApartmentSearch"""
from django.utils import timezone
from django.db.models import F
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from amenity.models import Amenity
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
    def get(self, request):
        """
        This method returns apartments that matches the search query
        entered by the user.
        """
        # pylint: disable=no-member

        # serializer = ApartmentSearchSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # validated_data = serializer.validated_data

        all_params = request.GET.dict()

        # save all amenities from request to a list.
        amenities = []
        for key in all_params:
            if key.startswith('amenities'):
                amenities.append(all_params[key])

        country = all_params.get('country')
        state = all_params.get('state')
        city = all_params.get('city')
        school = all_params.get('school')
        listing_type = all_params.get('listing_type')
        max_price = all_params.get('max_price')
        min_price = all_params.get('min_price')
        available_for = all_params.get('available_for')
        sort_type = all_params.get('sort_type')
        min_floor_num = all_params.get('min_floor_num')
        max_floor_num = all_params.get('max_floor_num')

        apartments = Apartment.objects.filter(
            is_taken=False,
            approval_status='accepted',
            advert_exp_time__gt=timezone.now()
        )

        if country is not None and country != "":
            apartments = apartments.filter(country=country)

        if state is not None and state != "":
            apartments = apartments.filter(state=state)

        if city is not None and city != "":
            apartments = apartments.filter(city=city)

        if school is not None and school != "":
            apartments = apartments.filter(school=school)

        if listing_type is not None and listing_type != "":
            apartments = apartments.filter(listing_type=listing_type)

        if available_for is not None and available_for != "":
            apartments = apartments.filter(available_for=available_for)

        if min_price is not None and min_price != "" and max_price is not None and max_price != "":
            apartments = apartments.filter(price__range=(min_price, max_price))
        elif (min_price is None or min_price == "") and max_price is not None and max_price != "":
            apartments = apartments.filter(price__lte=max_price)
        elif min_price is not None and min_price != "" and (max_price is None or max_price == ""):
            apartments = apartments.filter(price__gte=min_price)

        if min_floor_num is not None and min_floor_num != "" \
            and max_floor_num is not None and max_floor_num != "":
            apartments = apartments.filter(floor_number__range=(min_floor_num, max_floor_num))
        elif (min_floor_num is None or min_floor_num == "") \
            and max_floor_num is not None and max_floor_num != "":
            apartments = apartments.filter(floor_number__lte=max_floor_num)
        elif min_floor_num is not None and min_floor_num != "" \
            and (max_floor_num is None or max_floor_num == ""):
            apartments = apartments.filter(floor_number__gte=min_floor_num)

        if amenities:
            apartments = apartments.filter(amenities__name__in=amenities).distinct()

            for amenity_name in amenities:
                apartments = apartments.filter(amenities__name=amenity_name)

        # Order the apartments queryset by inverse of created_at
        if sort_type is None or sort_type == '':
            apartments = apartments.order_by('-created_at')
        elif sort_type in ('bedroom'):
            bedroom = Amenity.objects.get(name='bedroom')

            # Filter and get only apartments with bedrooms.
            # Adds a new field amenity_quantity to each filtered Apartment instance.
            # Sort the result based on value of sort type.
            apartments = apartments.filter(
                apartmentamenity__amenity=bedroom
            ).annotate(
                amenity_quantity=F('apartmentamenity__quantity')
            ).order_by('amenity_quantity')
        elif sort_type in ('-bedroom'):
            bedroom = Amenity.objects.get(name='bedroom')

            # Filter and get only apartments with bedrooms.
            # Adds a new field amenity_quantity to each filtered Apartment instance.
            # Sort the result based on value of sort type.
            apartments = apartments.filter(
                apartmentamenity__amenity=bedroom
            ).annotate(
                amenity_quantity=F('apartmentamenity__quantity')
            ).order_by('-amenity_quantity')
        else:
            apartments = apartments.order_by(sort_type)

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
