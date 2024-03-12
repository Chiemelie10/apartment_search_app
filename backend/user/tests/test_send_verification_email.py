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

        response = self.client.post(
            path=reverse('login_user'),
            data={
                'username': 'test_user',
                'password': 'password'
            },
            content_type='application/json'
        )

        self.access_token = response.json().get('access')
        self.headers = {'Authorization': f'Bearer {self.access_token}'}
        self.user = User.objects.get(username='test_user')

    def test_send_email(self):
        """
        This method tests that verification token is sent to the
        email address of the user.
        """
        response = self.client.get(
            path=reverse('email_verification_token'),
            headers=self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'FindAccommodation OTP')

        response_data = response.json()
        self.assertEqual(
            response_data.get('message'),
            f'A One Time Password (OTP) has been sent to {self.user.email}.'
        )

    def test_user_access_token_not_set(self):
        """
        This methods tests that a 404 http status code and an error
        message is returned when access token is not set in the header.
        """
        response = self.client.get(
            path=reverse('email_verification_token'),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(response.json().get('detail'),
                         'Authentication credentials were not provided.')

    def test_verification_token_in_email(self):
        """
        This method tests that a verification taken is created
        and sent in the body of the email.
        """
        response = self.client.get(
            path=reverse('email_verification_token'),
            headers=self.headers
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
        response = self.client.get(
            path=reverse('email_verification_token'),
            headers=self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = self.user.verification_token

        self.assertEqual(token.is_for_password_reset, False)
        self.assertEqual(token.is_used, False)
        self.assertEqual(token.is_validated_for_password_reset, False)
