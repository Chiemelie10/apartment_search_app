"""This module defines the endpoints related with the apartment app."""
from django.urls import path
from state.views.get_states import GetStatesView


urlpatterns = [
    path('api/states/all', GetStatesView.as_view(), name='get_states'),
]
