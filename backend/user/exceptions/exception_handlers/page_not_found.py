"""This module defines the function custom_404_view."""
from rest_framework import status
from rest_framework.response import Response


# pylint: disable=unused-argument
def custom_404_view(request, exception):
    """Returns an error message if wrong url was searched by the user."""
    return Response({'error': 'Page not found.'}, status=status.HTTP_404_NOT_FOUND)
