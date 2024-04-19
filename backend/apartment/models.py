"""This module defines class Apartment"""
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from country.models import Country
from state.models import State
from city.models import City
from school.models import School
from amenity.models import Amenity


User = get_user_model()

LISTING_TYPE_CHOICES = (
    ('roommate', 'roomate'),
    ('selfcontained', 'selfcontained'),
    ('non-selfcontained', 'non-selfcontained'),
    ('flat', 'flat'),
    ('bungalow', 'bungalow'),
    ('duplex', 'duplex'),
)

APPROVAL_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected')
)

class Apartment(models.Model):
    """This class defines the fields of the apartments table in the database."""
    id = models.CharField(default=uuid4, max_length=36,
                          unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='apartments', blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='apartments')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='apartments')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='apartments')
    amenities = models.ManyToManyField(Amenity, through='ApartmentAmenity')
    school = models.ForeignKey(School, on_delete=models.CASCADE,
                               related_name='apartments', null=True, blank=True)
    nearest_bus_stop = models.CharField(max_length=500)
    listing_type = models.CharField(max_length=500, choices=LISTING_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    is_taken = models.BooleanField(default=False)
    is_taken_time = models.DateTimeField(blank=True, null=True)
    is_taken_number = models.IntegerField(default=0, validators=[MaxValueValidator(limit_value=2)])
    video_link = models.CharField(max_length=5000, null=True, blank=True)
    approval_status = models.CharField(max_length=500, default='pending',
                                       choices=APPROVAL_STATUS_CHOICES, blank=True)
    advert_days_left = models.IntegerField(blank=True, default=0)
    advert_exp_time = models.DateTimeField(null=True, blank=True)
    num_of_exp_time_extension = models.IntegerField(default=0,
                                                    validators=[MaxValueValidator(limit_value=1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        db_table: Name of the table this class creates in the database.
        ordering: The order the instances of this model is displayed on the admin page.
        """
        db_table = 'apartments'
        ordering = ['-created_at']

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        return f'{self.id}'


class ApartmentAmenity(models.Model):
    """
    This class defines the fields of the junction table between
    apartments table and amenities table.
    """
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        db_table: Name of the table this class creates in the database.
        verbose_name_plural: Plural form of human readable name of the model in the admin page.
        ordering: The order the instances of this model is displayed on the admin page.
        """
        db_table = 'apartment_amenties'
        verbose_name_plural = 'Apartment amenities'
        ordering = ['-created_at']

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'Apartment_id: {self.apartment.id} - Amenity: {self.amenity.name}'
