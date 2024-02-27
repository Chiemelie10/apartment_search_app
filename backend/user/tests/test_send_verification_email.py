"""This module defines class SendVerificationEmailTest"""
from rest_framework import status
from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

class SendVerificationEmailTest(TestCase):
    """
    This class defines methods that test the functionality
    of the SendEmailVerificationToken.
    """

    def setUp(self):
        """
        This method is called before the start of each method of the class
        and destroyed at the end of each method.
        """
        data = {
            "username": "test_user",
            "email": "test_user@gmail.com",
            "password": "password"
        }

        self.client.post(
            path=reverse('register_user'),
            data=data,
            content_type="application/json"
        )

        self.user = User.objects.get(username='test_user')

    def test_send_email(self):
        """
        This method tests that verification token is sent to the
        email address of the user.
        """
        user_id = self.user.id

        response = self.client.get(
            path=reverse('email_verification_token', kwargs={'user_id': user_id}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'FindAccommodation OTP')

        response_data = response.json()
        self.assertEqual(
            response_data.get('message'),
            f'A One Time Password (OTP) has been sent to {self.user.email}.'
        )

    def test_user_not_found(self):
        """
        This methods tests that a 404 http status code and an error
        message is returned when the provided user_id is incorrect, ie
        no matching user with that id in the database.
        """
        response = self.client.get(
            path=reverse('email_verification_token', kwargs={'user_id': 'fake_user_id'}),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(mail.outbox), 0)

        response_data = response.json()
        self.assertEqual(response_data.get('error'), 'User not found.')

    def test_verification_token_in_email(self):
        """
        This method tests that a verification taken is created
        and sent in the body of the email.
        """
        user_id = self.user.id

        response = self.client.get(
            path=reverse('email_verification_token', kwargs={'user_id': user_id}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

        token = self.user.verification_token
        self.assertIn(token.verification_token, mail.outbox[0].body)

    def test_verification_token_set_values(self):
        """
        This method tests that the default values of the created token
        matches the ones set in the SendEmailVerificationToken view.
        """
        user_id = self.user.id

        response = self.client.get(
            path=reverse('email_verification_token', kwargs={'user_id': user_id}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = self.user.verification_token

        self.assertEqual(token.is_for_password_reset, False)
        self.assertEqual(token.is_used, False)
        self.assertEqual(token.is_validated_for_password_reset, False)
        self.assertEqual(token.otp_submission_time, None)
