"""This module defines the endpoints related with the apartment app."""
from django.urls import path
from apartment.views.create_apartment import CreateApartmentView
from apartment.views.get_apartments import GetApartmentsView
from apartment.views.get_available_apartments import GetAvailableApartmentsView
from apartment.views.apartment import ApartmentView


urlpatterns = [
    path('api/apartments/create', CreateApartmentView.as_view(), name='create_apartments'),
    path('api/apartments/all', GetApartmentsView.as_view(), name='get_apartments'),
    path('api/apartments/available', GetAvailableApartmentsView.as_view(),
         name='get_available_apartments'),
    path('api/apartments/<str:apartment_id>', ApartmentView.as_view(),
         name='get_update_delete_apartment'),
]
