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

def is_otp_submission_time_expired(token, exp_time_length):
    """
    This function returns True if the difference between time of submission of the token string
    and current time exceeds value of exp_time_length(seconds).
    It returns False if the difference is less than that value.
    """
    token_submitted_at = token.otp_submission_time
    current_time = timezone.now()

    time_difference = current_time - token_submitted_at

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
