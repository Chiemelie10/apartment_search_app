"""This module defines class GetCountriesView."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from country.models import Country
from country.serializers import CountryModelSerializer
from apartment.models import Apartment


class GetCountriesView(APIView):
    """This class defines a method that gets all the country objects from the database."""
    # pylint: disable=unused-argument

    @extend_schema(
        responses={200: CountryModelSerializer}
    )
    def get(self, request):
        """
        This method gets all countries from the database.\n
        Returns:\n
            On success: A http status code of 200 and data showing all countries,
            their states, cities and schools.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member

        # Get all countries
        # countries = Country.objects.all().order_by('-created_at')
        countries = Country.objects.filter(
            id__in=Apartment.objects.values('country')
        )

        # serialize countries
        serializer = CountryModelSerializer(countries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
