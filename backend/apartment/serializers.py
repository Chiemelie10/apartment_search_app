"""This module defines the serializer classes used for the apartment app."""
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from user.utils import check_html_tags, resize_image
from image.serializers import ImageSerializer
from image.models import Image
from country.models import Country
from country.serializers import CountrySerializer
from state.models import State
from state.serializers import StateSerializer
from city.models import City
from city.serializers import CitySerializer
from school.models import School
from school.serializers import SchoolModelSerializer
from amenity.models import Amenity
from amenity.serializers import AmenityModelSerializer
from user.serializers import UserSerializer
from .models import Apartment, ApartmentAmenity


class ApartmentAmenitySerializer(serializers.ModelSerializer):
    """
    This class defines class attributes of the ApartmentAmenity model
    to be validated when a request is made.
    """
    # pylint: disable=no-member
    apartment = serializers.PrimaryKeyRelatedField(read_only=True)
    amenity = AmenityModelSerializer(required=True)
    class Meta:
        """
            model: Name of the model.
            fields: The class attributes of the named model to be validated or serialized.
        """
        model = ApartmentAmenity
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    """This class defines the fields of the Apartment model to be validated and serialized."""
    # pylint: disable=no-member

    images = ImageSerializer(many=True, read_only=True)
    extend_time = serializers.BooleanField(default=False, write_only=True, required=False)
    advert_days_left = serializers.SerializerMethodField()
    advert_exp_time = serializers.DateTimeField(read_only=True)
    num_of_exp_time_extension = serializers.IntegerField(read_only=True)
    is_taken_time = serializers.DateTimeField(read_only=True)
    is_taken_number = serializers.IntegerField(read_only=True)
    user = UserSerializer(required=False)
    # country = serializers.PrimaryKeyRelatedField(
    #     required=True,
    #     queryset=Country.objects.prefetch_related('apartments').all()
    # )
    country = CountrySerializer(required=True)
    # state = serializers.PrimaryKeyRelatedField(
    #     required=True,
    #     queryset=State.objects.prefetch_related('apartments').all()
    # )
    state = StateSerializer(required=True)
    # city = serializers.PrimaryKeyRelatedField(
    #     required=True,
    #     queryset=City.objects.prefetch_related('apartments').all()
    # )
    city = CitySerializer(required=True)
    # school = serializers.PrimaryKeyRelatedField(
    #     required=False,
    #     allow_null=True,
    #     queryset=School.objects.prefetch_related('apartments').all()
    # )
    school = SchoolModelSerializer(required=False)
    image_upload = serializers.ListField(
        required = False,
        child = serializers.ImageField(max_length=500, use_url=False),
        write_only = True,
        allow_empty = True,
        allow_null=True,
    )
    image_delete = serializers.ListField(
        required = False,
        child = serializers.IntegerField(),
        write_only = True,
        allow_empty = True,
        allow_null=True,
    )
    amenities = ApartmentAmenitySerializer(
            required=True,
            many=True,
            allow_empty=True,
            source='apartmentamenity_set',
            allow_null=True
    )
    price = serializers.IntegerField(min_value=0, required=True)

    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = Apartment
        fields = [
            'id',
            'user',
            'country',
            'state',
            'city',
            'amenities',
            'school',
            'nearest_bus_stop',
            'listing_type',
            'size',
            'floor_number',
            'available_for',
            'price_duration',
            'title',
            'description',
            'price',
            'is_taken',
            'is_taken_time',
            'is_taken_number',
            'approval_status',
            'images',
            'image_upload',
            'image_delete',
            'video_link',
            'extend_time',
            'advert_days_left',
            'advert_exp_time',
            'num_of_exp_time_extension'
        ]

    def to_representation(self, instance):
        """
        This method is overridden to define data that is returned when
        object is serialized using the UserSerializer.
        """
        data = super().to_representation(instance)
        # Check if current user is the owner of the profile
        user = self.context['request'].user

        if user.is_staff is True:
            return data

        if user == instance.user:
            excluded_fields = [
                'is_taken_time',
                'is_taken_number',
                'advert_exp_time',
                'num_of_exp_time_extension'
            ]
            for field in excluded_fields:
                data.pop(field, None)

            return data

        if user != instance.user:
            excluded_fields = [
                'is_taken_time',
                'is_taken_number',
                'advert_exp_time',
                'num_of_exp_time_extension',
                'approval_status',
                'advert_days_left',
                'is_taken'
            ]
            for field in excluded_fields:
                data.pop(field, None)

            return data

    def validate(self, attrs):
        """
        This method validates the request and returns the value of the attrs in the request.
        """
        apartment = self.context.get('apartment')
        request_method = self.context['request'].method
        request_user = self.context['request'].user

        country = attrs.get('country')
        state = attrs.get('state')
        city = attrs.get('city')
        school = attrs.get('school')
        image_upload = attrs.get('image_upload')
        image_delete = attrs.get('image_delete')
        listing_type = attrs.get('listing_type')
        is_taken = attrs.get('is_taken')
        extend_time = attrs.get('extend_time')

        # Ensure country and state relationship
        if country is not None and state is not None:
            states = country.states.all()
            if state not in states:
                raise serializers.ValidationError('This state is not in the country entered.')

        # Ensure state and city relationship
        if state is not None and city is not None:
            cities = state.cities.all()
            if city not in cities:
                raise serializers.ValidationError('This city is not in the state entered.')

        # Ensure state and school relationship
        if state is not None and school is not None:
            state_of_school = school.state
            if state != state_of_school:
                raise serializers.ValidationError('This school is not in the state entered.')

        # Ensure image upload and delete operations cannot happen in the same request
        if image_upload is not None and image_upload != [] and \
            image_delete is not None and image_delete != []:
            raise serializers.ValidationError(
                'Image delete and upload operations is not allowed in the same request.'
            )

        if request_method == 'POST':
            # Ensure the value of image_upload field is not None for post request.
            if image_upload is None:
                raise serializers.ValidationError(
                    'The field "image_upload" is required when http method is post.'
                )

            # Ensure number of uploaded images is not greater than ten.
            if image_upload is not None:
                if len(image_upload) > 10:
                    raise serializers.ValidationError('Images cannot be more than ten.')

            # Ensure length of images is not less than 3 when listing
            # type is not roommate or non-selfcontained.
            if listing_type.lower() not in ('roommate', 'non-selfcontained'):
                if len(image_upload) < 3:
                    raise serializers.ValidationError(
                        'Images cannot be less than three for the entered listing type.'
                    )

            # Ensure length of images is not less than 2 when listing
            # type is roommate or non-selfcontained.
            if listing_type.lower() in ('roommate', 'non-selfcontained'):
                if len(image_upload) < 2:
                    raise serializers.ValidationError(
                        'Images cannot be less than two for the entered listing type.'
                    )

        # Validate number of images that will left after deletion
        if request_method in ('PUT', 'PATCH'):
            images = apartment.images.all()

            # Ensure total number of uploaded images and previous uploaded images
            # are not more than ten.
            if image_upload is not None:
                if len(images) + len(image_upload) > 10:
                    raise serializers.ValidationError(
                        'Ensure the total number of previously uploaded images and the ones '\
                        'you are trying to upload is not more than ten.'
                    )

            # Check for when listing type and images to be deleted are in the request body
            if image_delete is not None and listing_type is not None:
                if listing_type.lower() in ('roommate', 'non-selfcontained'):
                    if len(images) - len(image_delete) < 2:
                        raise serializers.ValidationError(
                            'Images left after deletion cannot be less than two.'
                        )
                if listing_type.lower() not in ('roommate', 'non-selfcontained'):
                    if len(images) - len(image_delete) < 3:
                        raise serializers.ValidationError(
                            'Images left after deletion cannot be less than three.'
                        )

            # Check for when listing type is not in the request body but there
            # are images to be deleted.
            if image_delete is not None and listing_type is None:
                listing_type = apartment.listing_type
                if listing_type.lower() in ('roommate', 'non-selfcontained'):
                    if len(images) - len(image_delete) < 2:
                        raise serializers.ValidationError(
                            'Images left after deletion cannot be less than two.'
                        )
                if listing_type.lower() not in ('roommate', 'non-selfcontained'):
                    if len(images) - len(image_delete) < 3:
                        raise serializers.ValidationError(
                            'Images left after deletion cannot be less than three.'
                        )

            # Reset is_taken_time and is_taken_number values when is_taken is True
            # It is for limiting the number of times the owner of an advert can switch
            # is_taken value on and off and limiting a user from setting is_taken False
            # after a certain time has elapsed.
            if is_taken is True and request_user == apartment.user:
                current_is_taken_value = apartment.is_taken
                if current_is_taken_value is False:
                    attrs['is_taken_time'] = timezone.now()
                    attrs['is_taken_number'] = apartment.is_taken_number + 1

            if is_taken is False and request_user == apartment.user:
                current_is_taken_value = apartment.is_taken
                if current_is_taken_value is True:
                    is_taken_time = apartment.is_taken_time
                    is_taken_number = apartment.is_taken_number
                    if is_taken_time >= is_taken_time + timedelta(days=1):
                        raise serializers.ValidationError(
                            'The field "is_taken" cannot be set to false on or after 24 hours.'
                        )
                    if is_taken_number >= 2:
                        raise serializers.ValidationError(
                            'The field "is_taken" cannot be set to false after '\
                            'setting it to True twice.'
                        )
                    attrs['is_taken_time'] = None
                    attrs['is_taken_number'] = is_taken_number

            # Check if advert is going to be extended more than once.
            if extend_time is True:
                num_of_exp_time_extension = apartment.num_of_exp_time_extension
                if num_of_exp_time_extension >= 1:
                    raise serializers.ValidationError(
                        'Advert cannot be extended more than once.'
                    )

        return attrs

    @extend_schema_field(serializers.IntegerField())
    def get_advert_days_left(self, obj):
        """Returns number of days left for the apartment object advert to expiration."""
        return obj.advert_days_left

    def validate_amenities(self, amenities):
        """
        This method validates the list of amenities before converting it
        from a list of dictionary to a list.
        NB: To ensure no amenities, ie to set the value of amenities to be "none"
            amenity object created and saved in the database, make the value of
            amenities in the boby request to be [] or null or the id of None amenity object.
        """
        # Validate list of amenities
        if amenities is None:
            amenities = []

        for amenity in amenities:
            value = amenity.get('amenity')
            quantity = amenity.get('quantity')
            if quantity is None:
                raise serializers.ValidationError(
                    'The field "quantity" is required.'
                )
            if value.name.lower() == 'none':
                if len(amenities) > 1:
                    raise serializers.ValidationError(
                        'There cannot be more than one amenity when "None" is entered.'
                    )
                if quantity != 0:
                    raise serializers.ValidationError(
                        'The value of quantity must be zero when amenity is none.'
                    )
            if value.name.lower() != 'none':
                if quantity <= 0:
                    raise serializers.ValidationError(
                        'The value of quantity must be greater than zero when amenity is not none.'
                    )

        # Add none to list of amenities if empty list was submitted.
        if amenities == []:
            amenity = Amenity.objects.get(name='None')
            amenities.append({'amenity': amenity, 'quantity': 0})

        return amenities

    def validate_title(self, title):
        """This method does extra validation on the title field."""
        # Check for html tags in submitted title.
        is_html_in_value, validated_value = check_html_tags(title)

        if is_html_in_value is True:
            raise serializers.ValidationError(
                'html tags or anything similar is not allowed. '\
                'Remove all angular brackets to proceed.'
            )

        return validated_value

    def validate_description(self, description):
        """This method does extra validation on the description field."""
        # Check for html tags in submitted description.
        is_html_in_value, validated_value = check_html_tags(description)

        if is_html_in_value is True:
            raise serializers.ValidationError(
                'html tags or anything similar is not allowed. '\
                'Remove all angular brackets to proceed.'
            )

        return validated_value

    def validate_nearest_bus_stop(self, nearest_bus_stop):
        """This method does extra validation on the nearest_bus_stop field."""
        # Check for html tags in submitted title.
        is_html_in_value, validated_value = check_html_tags(nearest_bus_stop)

        if is_html_in_value is True:
            raise serializers.ValidationError(
                'html tags or anything similar is not allowed. '\
                'Remove all angular brackets to proceed.'
            )

        return validated_value

    def validate_image_upload(self, image_upload):
        """This method validates and resizes the images."""
        request_method = self.context['request'].method

        if request_method in ('PUT', "PATCH"):
            apartment = self.context.get('apartment')
            user = self.context['request'].user

            # Ensure staff cannot upload images for a user when updating
            if user != apartment.user and user.is_staff is True:
                return None

        if image_upload is None:
            image_upload = []

        resized_images = []
        allowed_mimetypes = ['image/jpeg']

        for image in image_upload:
            if image.content_type not in allowed_mimetypes:
                raise serializers.ValidationError('Invalid mime type. Only image/jpeg can be used.')

        for image in image_upload:
            resized_image = resize_image(image=image, new_width=400)
            resized_images.append(resized_image)

        return resized_images

    def validate_image_delete(self, images_id_to_delete):
        """
        This method validates the image ids in the image_delete list.
        It also converts the ids to image objects, enters them in a
        new list and returns the new list.
        """
        apartment = self.context.get('apartment')
        request_method = self.context['request'].method
        user = self.context['request'].user

        if request_method == 'PUT' or request_method == 'PATCH':
            if user != apartment.user and user.is_staff is True:
                return None

            if images_id_to_delete is not None and images_id_to_delete != []:
                image_delete = Image.objects.filter(pk__in=images_id_to_delete, apartment=apartment)
                if len(image_delete) != len(images_id_to_delete):
                    if len(images_id_to_delete) == 1:
                        raise serializers.ValidationError(
                            'The image you are trying to delete was not found. Ensure '\
                            'the id of the image and apartment is correct.'
                        )
                    raise serializers.ValidationError(
                        'One or more of the images you are trying to delete was not found. '\
                        'Ensure the id of each of the images and that of the apartment is correct.'
                    )
                return image_delete
        return images_id_to_delete


class ApartmentSearchSerializer(serializers.ModelSerializer):
    """This class defines the fields of the Apartment model to be validated and serialized."""
    # pylint: disable=no-member
    country = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        queryset=Country.objects.prefetch_related('apartments').all()
    )
    state = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        queryset=State.objects.prefetch_related('apartments').all()
    )
    city = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        queryset=City.objects.prefetch_related('apartments').all()
    )
    school = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        queryset=School.objects.prefetch_related('apartments').all()
    )
    amenities = ApartmentAmenitySerializer(
            required=False,
            many=True,
            allow_empty=True,
            source='apartmentamenity_set',
            allow_null=True
    )
    max_price = serializers.IntegerField(min_value=0, allow_null=True, required=False)
    min_price = serializers.IntegerField(min_value=0, allow_null=True, required=False)
    listing_type = serializers.CharField(required=False, allow_null=True)

    class Meta:
        """
            model: Name of the model
            fields: The class attributes of the above name model
                    to be validated
        """
        model = Apartment
        fields = [
            'country',
            'state',
            'city',
            'amenities',
            'school',
            'listing_type',
            'max_price',
            'min_price'
        ]

    def to_representation(self, instance):
        """
        This method is overridden to define data that is returned when
        object is serialized using the UserSerializer.
        """
        data = super().to_representation(instance)
        # Check if current user is the owner of the profile
        user = self.context['request'].user

        if user.is_staff is True:
            return data

        if user == instance.user:
            excluded_fields = [
                'is_taken_time',
                'is_taken_number',
                'advert_exp_time',
                'num_of_exp_time_extension'
            ]
            for field in excluded_fields:
                data.pop(field, None)

            return data

        if user != instance.user:
            excluded_fields = [
                'is_taken_time',
                'is_taken_number',
                'advert_exp_time',
                'num_of_exp_time_extension',
                'approval_status'
            ]
            for field in excluded_fields:
                data.pop(field, None)

            return data

    def validate(self, attrs):
        """
        This method validates the request and returns the value of the attrs in the request.
        """
        # country = attrs.get('country')
        # state = attrs.get('state')
        # city = attrs.get('city')
        # school = attrs.get('school')
        # listing_type = attrs.get('listing_type')
        max_price = attrs.get('max_price')
        min_price = attrs.get('min_price')
        amenities = attrs.get('apartmentamenity_set')

        if amenities == []:
            amenities = None

        # if country is None and state is None and city is None\
        # and school is None and listing_type is None and max_price is None\
        # and min_price is None and amenities is None:
        #     raise serializers.ValidationError(
        #         'The fields and values to be seached are required.'
        #     )

        if min_price is not None and max_price is None:
            raise serializers.ValidationError('The field "Max_price" is required.')

        return attrs
