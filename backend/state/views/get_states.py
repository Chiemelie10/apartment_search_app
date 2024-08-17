"""This module defines class GetStatesView."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from state.models import State
from state.serializers import StateModelSerializer
from apartment.models import Apartment


class GetStatesView(APIView):
    """This class defines a method that gets all the state objects from the database."""
    # pylint: disable=unused-argument

    @extend_schema(
        responses={200: StateModelSerializer}
    )
    def get(self, request):
        """
        This method gets states from the database.\n
        Returns:\n
            On success: A http status code of 200 and data showing all
            states that have apartments, their cities and schools.\n
            On failure: An error message with a corresponding http status code.
        """
        # pylint: disable=no-member

        # Get all countries
        # countries = Country.objects.all().order_by('-created_at')
        states = State.objects.filter(
            id__in=Apartment.objects.values('state')
        )

        # serialize countries
        serializer = StateModelSerializer(states, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
