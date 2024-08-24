"""This module defines class Apartment"""
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.utils import timezone
from country.models import Country
from state.models import State
from city.models import City
from school.models import School
from amenity.models import Amenity


User = get_user_model()

LISTING_TYPE = (
    ('self-contained', 'Self-contained'),
    ('non-self-contained', 'Non-self-contained'),
    ('flat', 'Flat'),
    ('bungalow', 'Bungalow'),
    ('duplex', 'Duplex'),
)

FLOOR_NUMBER = (
    (0, 'Ground floor'),
    (1, 'First floor'),
    (2, 'Second floor'),
    (3, 'Third floor'),
    (4, 'Fourth floor'),
    (5, 'Fifth floor'),
    (6, 'Sixth floor'),
    (7, 'Seventh floor'),
    (8, 'Eighth floor'),
    (9, 'Nineth floor'),
    (10, 'Tenth floor'),
    (11, 'Eleventh floor'),
    (12, 'Twelfth floor'),
    (13, 'Thirteenth floor'),
    (14, 'Fourteenth floor'),
    (15, 'Fifteenth floor'),
    (16, 'Sixteenth floor'),
    (17, 'Seventeenth floor'),
    (18, 'Eighteenth floor'),
    (19, 'Nineteenth floor'),
    (20, 'Twentieth floor')
)

AVAILABLE_FOR = (
    ('share', 'Share'),
    ('short let', 'Short let'),
    ('rent', 'Rent'),
    ('lease', 'Lease'),
    ('sale', 'Sale'),
)

PRICE_DURATION = (
    ('hour', 'Hour'),
    ('day', 'Day'),
    ('week', 'Week'),
    ('month', 'Month'),
    ('year', 'Year')
)

APPROVAL_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected')
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
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    nearest_bus_stop = models.CharField(max_length=500)
    price = models.IntegerField()
    size = models.CharField(max_length=500, null=True, blank=True)
    floor_number = models.IntegerField(choices=FLOOR_NUMBER, null=True, blank=True)
    listing_type = models.CharField(max_length=500, choices=LISTING_TYPE)
    available_for = models.CharField(max_length=500, choices=AVAILABLE_FOR)
    price_duration = models.CharField(max_length=500, choices=PRICE_DURATION)
    is_featured = models.BooleanField(default=False)
    is_taken = models.BooleanField(default=False)
    is_taken_time = models.DateTimeField(blank=True, null=True)
    is_taken_number = models.IntegerField(default=0, validators=[MaxValueValidator(limit_value=2)])
    video_link = models.CharField(max_length=5000, null=True, blank=True)
    approval_status = models.CharField(max_length=500, default='pending',
                                       choices=APPROVAL_STATUS_CHOICES, blank=True)
    # advert_days_left = models.IntegerField(blank=True, default=0)
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

    @property
    def advert_days_left(self):
        """Calculate the number of days left until expiration."""
        if self.advert_exp_time is None:
            return 0
        delta = self.advert_exp_time - timezone.now()
        return max(delta.days, 0)

class ApartmentAmenity(models.Model):
    """
    This class defines the fields of the junction table between
    apartments table and amenities table.
    """
    id = models.CharField(default=uuid4, max_length=36,
                          unique=True, primary_key=True, editable=False)
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
