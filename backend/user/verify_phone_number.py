"""This module defines functions that validates a user's phone number."""
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_SERVICE_SID)


def send_phone_otp(phone):
    """This function sends OTP to the phone number provided."""
    verify.verifications.create(to=phone, channel='sms')


def check_phone_otp(phone, code):
    """
    This function confirms that the OTP submitted by the user
    matches the one sent to the user's phone number.
    """
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        return False

    return result.status == 'approved'
