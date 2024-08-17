"""This module defines the endpoints related with the apartment app."""
from django.urls import path
from country.views.get_countries import GetCountriesView


urlpatterns = [
    path('api/countries/all', GetCountriesView.as_view(), name='get_countries'),
]
