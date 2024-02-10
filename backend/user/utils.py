"""This module defines some helper functions and classes for the user_app app."""
# import threading
from random import randint
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.utils.html import strip_tags
from user_verification_token.models import VerificationToken


def token_generator():
    """This function returns a randomly generated number."""
    return str(randint(1000000, 9999999))


def send_email_verification_link(user):
    """This function sends link for email verification to the user."""
    # pylint: disable=no-member
    # pylint: disable=broad-exception-caught

    email_subject = 'FindAccommodation OTP'
    token = token_generator()
    email_body = render_to_string('user/verify_email.html', {
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
