"""This module defines class UtilsFuntionsTest"""
import time
from django.utils import timezone
from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from user_verification_token.models import VerificationToken
from user.utils import (
    token_generator,
    send_verification_token,
    is_token_expired,
    is_otp_submission_time_expired,
    check_html_tags
)


User = get_user_model()

class UtilsFunctionsTest(TestCase):
    """This class defines methods that tests each function the utils.py file."""

    @classmethod
    def setUpTestData(cls):
        """
        This method sets up non-modified objects used by all test
        methods in which the user object is used. It does this only once.
        """

        cls.user = User.objects.create_user(
            username = 'test_user',
            email = 'test_user@gmail.com',
            password = 'password'
        )

    def test_token_generator(self):
        """
        This method tests that generated tokens are always unique in given sample.
        """
        # pylint: disable=no-member

        tokens = []
        for i in range(1, 51):
            token = token_generator()

            user = User.objects.create_user(
                username=f"test_user{i}",
                email=f"testuser{i}@gmail.com",
                password="test_user_password"
            )

            VerificationToken.objects.create(user=user, verification_token=token)
            tokens.append(token)

        self.assertEqual(len(tokens), 50)
        self.assertEqual(len(tokens), len(set(tokens)))

    def test_send_verification_token(self):
        """
        This method tests that a verification token for email verification is created.
        it also tests that the email was successfully sent.
        """
        # pylint: disable=no-member

        user = UtilsFunctionsTest.user

        # Test there is no token in the database before sending of the email
        tokens = VerificationToken.objects.all()
        self.assertFalse(tokens.exists())
        self.assertEqual(len(tokens), 0)

        # send verification token to email
        send_verification_token(user=user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'FindAccommodation OTP')

        # Test verification token is now in the database after sending of email
        tokens = VerificationToken.objects.all()
        self.assertTrue(tokens.exists())
        self.assertEqual(len(tokens), 1)

        # Test default values of created token meets the requirement
        token = VerificationToken.objects.get(user=user)
        self.assertFalse(token.is_for_password_reset)
        self.assertFalse(token.is_used)
        self.assertFalse(token.is_validated_for_password_reset)
        self.assertEqual(token.otp_submission_time, None)
        self.assertEqual(len(token.verification_token), 7)
        self.assertIn(token.verification_token, mail.outbox[0].body)

    def test_is_token_expired(self):
        """
        This method tests the 'is_token_expired' function, which returns True
        if token has expired or False if not expired.
        '"""
        # pylint: disable=no-member

        user = UtilsFunctionsTest.user

        otp = token_generator()
        token = VerificationToken.objects.create(user=user, verification_token=otp)
        time.sleep(3)
        token_expired = is_token_expired(token, 2)
        self.assertEqual(token_expired, True)

        second_otp = token_generator()
        token.verification_token = second_otp
        token.save()
        token_expired = is_token_expired(token, 2)
        self.assertEqual(token_expired, False)

    def test_is_otp_submission_time_expired(self):
        """
        This method tests the 'is_otp_submission_time_expired' function. It
        returns True if the difference in time, from when a password-reset token
        was validated, exceeds the provided "expiry_time_length". It returns False
        when it has not exceeded.
        '"""
        # pylint: disable=no-member

        user = UtilsFunctionsTest.user

        otp = token_generator()
        token = VerificationToken.objects.create(user=user, verification_token=otp)
        token.otp_submission_time = timezone.now()
        token.save()
        time.sleep(3)
        token_expired = is_otp_submission_time_expired(token, 2)
        self.assertEqual(token_expired, True)

        second_otp = token_generator()
        token.verification_token = second_otp
        token.otp_submission_time = timezone.now()
        token.save()
        token_expired = is_otp_submission_time_expired(token, 2)
        self.assertEqual(token_expired, False)

    def test_check_html_tag(self):
        """
        This method tests the "check_html_tag" function. It returns True
        if html tag is present in a string or False if it isn't. It also
        returns the stripped string.
        """
        html_tag_in_str, _ = check_html_tags('<h1>password</h1>')
        self.assertEqual(html_tag_in_str, True)

        html_tag_in_str, _ = check_html_tags('<script>password</script>')
        self.assertEqual(html_tag_in_str, True)

        html_tag_in_str, _ = check_html_tags('password</b>')
        self.assertEqual(html_tag_in_str, True)

        html_tag_in_str, _ = check_html_tags('<p>password')
        self.assertEqual(html_tag_in_str, True)

        html_tag_in_str, _ = check_html_tags('<password>')
        self.assertEqual(html_tag_in_str, True)

        html_tag_in_str, _ = check_html_tags('<p>password<p>')
        self.assertEqual(html_tag_in_str, True)

        html_tag_in_str, _ = check_html_tags('<1>password</1>')
        self.assertEqual(html_tag_in_str, True)

        html_tag_in_str, _ = check_html_tags('password')
        self.assertEqual(html_tag_in_str, False)

        html_tag_in_str, _ = check_html_tags('<>password<>')
        self.assertEqual(html_tag_in_str, False)

        html_tag_in_str, _ = check_html_tags('<1>password<1>')
        self.assertEqual(html_tag_in_str, False)

        html_tag_in_str, _ = check_html_tags('<#>password<#>')
        self.assertEqual(html_tag_in_str, False)
