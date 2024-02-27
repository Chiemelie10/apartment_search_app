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
            'username': 'Test_user',
            'email': 'test_user@gmail.com',
            'password': 'password'
        }

        self.client.post(
            path=reverse('register_user'),
            data=data,
            content_type='application/json'
        )

        self.user = User.objects.get(username='test_user')

        self.request_body = {
            'username': 'test_user'
        }

    def test_response_for_valid_username(self):
        """
        This method tests that verification token is sent to the
        email address of the user if a valid username is used in the
        body of the request.
        """
        response = self.client.post(
            path=reverse('forgot_password_token'),
            data=self.request_body,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'FindAccommodation OTP')

        response_data = response.json()
        self.assertEqual(
            response_data.get('message'),
            f'A One Time Password (OTP) has been sent to {self.user.email}.'
        )

    def test_response_for_valid_email(self):
        """
        This method tests that verification token is sent to the
        email address of the user if a valid email address is used
        in the body of the request.
        """
        request_body = self.request_body
        del request_body['username']
        request_body['email'] = 'test_user@gmail.com'

        response = self.client.post(
            path=reverse('forgot_password_token'),
            data=request_body,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'FindAccommodation OTP')

        response_data = response.json()
        self.assertEqual(
            response_data.get('message'),
            f'A One Time Password (OTP) has been sent to {self.user.email}.'
        )

    def test_response_for_empty_request_body(self):
        """
        This method tests that a 400 http status code and error message are returned
        if the request body is empty.
        """
        request_body = self.request_body
        del request_body['username']

        response = self.client.post(
            path=reverse('forgot_password_token'),
            data=request_body,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

        response_data = response.json()
        self.assertEqual(response_data['non_field_errors'][0], 'Email or username is required.')

    def test_response_for_using_email_and_username(self):
        """
        This method tests that a 400 http status code and error messages ar returned
        if the request body is contains both username and email.
        """
        request_body = self.request_body
        request_body['email'] = 'test_user@gmail.com'

        response = self.client.post(
            path=reverse('forgot_password_token'),
            data=request_body,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

        response_data = response.json()
        self.assertEqual(response_data['non_field_errors'][0],
                         'Provide either email or username, not both.')

    def test_response_for_invalid_username(self):
        """
        This methods tests that a 404 http status code and an error
        message is returned when the provided username is incorrect, ie
        no matching username is found in the database.
        """
        request_body = self.request_body
        request_body['username'] = 'wrong_username'

        response = self.client.post(
            path=reverse('forgot_password_token'),
            data=request_body,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(mail.outbox), 0)

        response_data = response.json()
        self.assertEqual(response_data.get('error'), 'User not found.')

    def test_response_for_invalid_email(self):
        """
        This methods tests that a 404 http status code and an error
        message is returned when the provided email is incorrect, ie
        no matching email is found in the database.
        """
        request_body = self.request_body
        del request_body['username']
        request_body['email'] = 'wrong_email@gmail.com'

        response = self.client.post(
            path=reverse('forgot_password_token'),
            data=request_body,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(mail.outbox), 0)

        response_data = response.json()
        self.assertEqual(response_data.get('error'), 'User not found.')

    def test_verification_token_set_values(self):
        """
        This method tests that the default values of the created token
        matches the ones set in the SendPasswordResetToken view.
        """
        request_body = self.request_body

        response = self.client.post(
            path=reverse('forgot_password_token'),
            data=request_body,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = self.user.verification_token

        self.assertEqual(token.is_for_password_reset, True)
        self.assertEqual(token.is_used, False)
        self.assertEqual(token.is_validated_for_password_reset, False)
        self.assertEqual(token.otp_submission_time, None)
