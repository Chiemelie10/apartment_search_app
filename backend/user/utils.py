"""This module defines some helper functions and classes for the user_app app."""
import os
from io import BytesIO
from random import randint
from PIL import Image, ImageOps
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.utils.html import strip_tags
from user_verification_token.models import VerificationToken


def token_generator():
    """This function returns a randomly generated number."""
    # pylint: disable=no-member

    while True:
        new_token = str(randint(1000000, 9999999))

        if not VerificationToken.objects.filter(verification_token=new_token).exists():
            return new_token

def send_verification_token(user, for_password=False):
    """This function sends link for email verification to the user."""
    # pylint: disable=no-member
    # pylint: disable=broad-exception-caught

    email_subject = 'FindAccommodation OTP'
    token = token_generator()

    if for_password is False:
        email_body = render_to_string('user/verify_email.html', {
            'user': user,
            'token': token
        })
    else:
        email_body = render_to_string('user/forgot_password.html', {
            'user': user,
            'token': token
        })

    email = EmailMultiAlternatives(
        subject=email_subject,
        body=strip_tags(email_body),
        from_email='findaccommodation.online@gmail.com',
        to=[user.email]
    )

    email.attach_alternative(email_body, "text/html")

    try:
        email.send()
        verification_token_obj = VerificationToken.objects.get(user=user)
        verification_token_obj.verification_token = token
        verification_token_obj.save()
    except VerificationToken.DoesNotExist:
        VerificationToken.objects.create(user=user, verification_token=token)
    except Exception as e:
        raise e


def is_token_expired(token, exp_time_length):
    """
    This function returns True if the difference between time of creation of
    token object and current time exceeds value of exp_time_length(seconds).
    It returns False if the difference is less than that value.
    """
    token_created_at = token.created_at
    current_time = timezone.now()

    time_difference = current_time - token_created_at

    if time_difference.total_seconds() > exp_time_length:
        return True
    return False

def check_html_tags(value):
    """
    This function returns True if a html tag is present in the string value
    passed into the function. Otherwise, it returns false.
    """
    stripped_string = strip_tags(value)
    return value != stripped_string, stripped_string

def get_tokens_for_user(user):
    """This method generates refresh and access tokens for a user."""
    # pylint: disable=no-member

    refresh = RefreshToken.for_user(user)
    role = user.profile.role
    if role is None:
        refresh['user_role'] = None
    else:
        refresh['user_role'] = role.name

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def blacklist_outstanding_tokens(user):
    """This function blacklists all outstanding tokens belonging to a user."""
    # pylint: disable=broad-exception-caught
    # pylint: disable=no-member

    outstanding_tokens = OutstandingToken.objects.filter(user=user)
    if outstanding_tokens.exists():
        for token in outstanding_tokens:
            BlacklistedToken.objects.get_or_create(token=token)

def resize_image(image, new_width):
    """This method resizes all thumbnail images to a specified size."""
    # Open the image using pillow
    img = Image.open(image)
    img = img.convert('RGB')

    aspect_ratio = img.width / img.height

    if img.width > new_width:
        # Resize the image while maintaining the aspect ratio
        new_height = int(new_width / aspect_ratio)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    else:
        resized_img = img

    # Enters the EXIF (Exchangeable Image File Format)
    # data of the image into the resized image.
    resized_img = ImageOps.exif_transpose(resized_img)

    # Compress image to reduce the file size
    content_type = image.content_type
    output_buffer = BytesIO()
    resized_img.save(output_buffer, format='JPEG', quality=85)
    output_buffer.seek(0)

    # Create a ContentFile from BytesIO buffer
    content_file = ContentFile(output_buffer.read())

    # Add extension to image name if image has no extension
    image_extension = os.path.splitext(image.name)[1]
    if image_extension == '':
        image.name = f'{image.name}.jpg'

    # Create an InMemoryUploadFile from the ContentFile
    resized_file = InMemoryUploadedFile(
        file=content_file,
        field_name=None,
        name=image.name,
        content_type=content_type,
        size=content_file.size,
        charset=None,
        content_type_extra=None
    )

    return resized_file
