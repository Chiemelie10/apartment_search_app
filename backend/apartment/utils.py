"""This module defines the functions utilized in the apartment app."""
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import default_storage
from django.urls import reverse
from django.utils import timezone
from image.models import Image
from .models import ApartmentAmenity


def paginate_queryset(queryset, page, page_size):
    """
    This function defines the number of adverts to be returned
    per page.
    """
    paginator = Paginator(queryset, per_page=page_size, orphans=0)
    try:
        paginated_data = paginator.page(page)
        total_pages = paginator.num_pages
        return paginated_data, total_pages
    except EmptyPage as exc:
        raise ValueError('Page not found.') from exc
    except PageNotAnInteger as exc:
        raise ValueError('Page number must be an integer.') from exc

def get_page_and_size(request):
    """
    This function checks if the value for page and page_size are int. it raises an
    exception if any of the two is not an int, returns value of page and page_size if both
    are int, and sets default values for one or both variables if not provided.
    """
    page = request.GET.get('page')
    page_size = request.GET.get('size')

    if page is None and page_size is None:
        return page, page_size

    if page is not None:
        # Raise exception if page is not an int
        try:
            page = int(page)
        except ValueError as exc:
            raise ValueError('Value for "page" must be an int.') from exc

    if page_size is not None:
        # Raise exception if page_size is not an int
        try:
            page_size = int(page_size)
        except ValueError as exc:
            raise ValueError('Value for "size" must be an int.') from exc

    # Set default page value if none was provided.
    if page is None:
        page = 1

    # Set default page_size value if none was provided.
    if page_size is None:
        page_size = 4

    return page, page_size

def get_prev_and_next_page(request, page, page_size, total_pages, url_name):
    """
    This function returns the value for previous and next page which will be
    added to the json response that will be returned.
    """
    if page == 1 and page == total_pages:
        previous_page = None
        next_page = None
    elif page == 1 and page < total_pages:
        previous_page = None
        next_page = f"https://{get_current_site(request).domain}"\
                    f"{reverse(url_name)}?page={page + 1}&size={page_size}"
    if page > 1 and page < total_pages:
        previous_page = f"https://{get_current_site(request).domain}"\
                        f"{reverse(url_name)}?page={page - 1}"\
                        f"&size={page_size}"
        next_page = f"https://{get_current_site(request).domain}"\
                    f"{reverse(url_name)}?page={page + 1}&size={page_size}"
    if page > 1 and page == total_pages:
        previous_page = f"https://{get_current_site(request).domain}"\
                        f"{reverse('get_available_apartments')}?page={page - 1}"\
                        f"&size={page_size}"
        next_page = None

    return previous_page, next_page

def save_apartment_amenities(amenities, apartment):
    """This function saves a list of submitted amenities for an apartment to the database."""
    # pylint: disable=no-member

    if amenities is not None:
        # Get all previously saved amenities for the apartment.
        apartment_amenities = ApartmentAmenity.objects.filter(apartment=apartment)

        if apartment_amenities.exists():
            # Add to the database the submitted amenities that are not in the list
            # of apartment_amenities.
            # Also converts from list of dictionaries to a list of amenity objects
            amenity_obj_list = []
            for amenity in amenities:
                amenity_obj = amenity['amenity']
                quanity = amenity['quantity']
                amenity_obj_list.append(amenity_obj)
                if amenity_obj not in apartment_amenities:
                    apartment.amenities.add(amenity_obj, through_defaults={'quantity': quanity})

            # Delete from the database the amenities that are not submitted.
            for apartment_amenity in apartment_amenities:
                if apartment_amenity.amenity not in amenity_obj_list:
                    apartment.amenities.remove(apartment_amenity.amenity)
                else:
                    for amenity in amenities:
                        amenity_obj = amenity['amenity']
                        quanity = amenity['quantity']
                        if amenity_obj == apartment_amenity.amenity and \
                            quanity != apartment_amenity.quantity:
                            apartment_amenity.quantity = quanity
                            apartment_amenity.save()
                            break
                        if amenity_obj == apartment_amenity.amenity and \
                            quanity == apartment_amenity.quantity:
                            break
        else:
            # Add amenities to the apartment when it has no previous captured amenities.
            for amenity in amenities:
                amenity_obj = amenity['amenity']
                quanity = amenity['quantity']
                apartment.amenities.add(amenity_obj, through_defaults={'quantity': quanity})

def save_apartment_images(images_to_upload, apartment):
    """
    This function saves each image of an apartment in the images_to_upload
    list to the database.
    """
    # pylint: disable=no-member
    if images_to_upload is not None:
        for image in images_to_upload:
            Image.objects.create(apartment=apartment, image=image)

def delete_apartment_images(images_to_delete):
    """
    This function deletes each image in the images_to_delete list
    from the database and file storage.
    """
    if images_to_delete is not None:
        for image in images_to_delete:
            image_path = image.image.path
            if default_storage.exists(image_path):
                default_storage.delete(image_path)
            image.delete()

def reset_advert_exp_time(apartment, extend_time=False):
    """
    This function resets the time remaining for an apartment advert
    and sets is_taken to True.
    """
    if extend_time is True:
        advert_days_left = apartment.advert_days_left
        advert_exp_time = apartment.advert_exp_time

        if advert_days_left != 0 and advert_exp_time is not None:
            # extend advert expiration time by a week
            advert_days_left = advert_days_left + 7
            advert_exp_time = advert_exp_time + timedelta(weeks=1)
            apartment.num_of_exp_time_extension = apartment.num_of_exp_time_extension + 1
            apartment.advert_exp_time = advert_exp_time
            apartment.advert_days_left = advert_days_left
    else:
        advert_days_left = apartment.advert_days_left
        advert_exp_time = apartment.advert_exp_time

    # Check if advert has expired and reset time
    if advert_days_left != 0 and advert_exp_time is not None:
        if timezone.now() >= advert_exp_time:
            apartment.advert_days_left = 0
            apartment.advert_exp_time = None
        else:
            time_difference = str(advert_exp_time - timezone.now())
            time_remaining_values = time_difference.split(' ')

            # Check if only time is left in time_remaining_values, giving it a length of 1.
            if len(time_remaining_values) == 1:
                apartment.advert_days_left = 1
            else:
                # Get days and time remaining values from time_difference
                days_remaining = int(time_remaining_values[0])
                time_remaining = time_remaining_values[-1]

                # Get hour and minute from time_remaining
                time_remaining_values = time_remaining.split(':')
                if len(time_remaining_values) < 3:
                    apartment.advert_days_left = days_remaining
                else:
                    hour = int(time_remaining_values[0])
                    minute = int(time_remaining_values[1])
                    if hour != 0 and minute != 0:
                        apartment.advert_days_left = days_remaining + 1

        apartment.save()
