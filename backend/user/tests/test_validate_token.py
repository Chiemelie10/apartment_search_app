"""This module defines class ValidateEmailTokenTest and ValidatePasswordTokenTest"""
import time
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()

class ValidateEmailTokenTest(TestCase):
    """This class defines methods that tests ValidateEmailVerificationTokenView class."""

    def setUp(self):
        """
        This method is called before the start of each method of the class
        and destroyed at the end of each method.
        """
        data = {
            'username': 'test_user',
            'email': 'test_user@gmail.com',
            'password': 'password'
        }

        self.client.post(
            path=reverse('register-user'),
            data=data,
            content_type='application/json'
        )

        self.user = User.objects.get(username='Test_user')

        self.client.get(
            path=reverse('email-verification-token', kwargs={'user_id': self.user.id}),
        )

        self.token = self.user.verification_token
        self.request_data = {'verification_token': self.token.verification_token}

        # Overide setting for time of expiration of otp
        settings.OTP_EXP_TIME = 2 # Two seconds

    def test_response_for_valid_token(self):
        """
        This method tests that a http status code of 200 and a success message is
        returned if a valid One Time Password (OTP) is submitted by the user. 
        """
        response = self.client.post(
            path=reverse('verify-email'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Email verified successfully.')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.verification_token.is_used, True)
        self.assertEqual(user.verification_token.is_for_password_reset, False)
        self.assertEqual(user.verification_token.is_validated_for_password_reset, False)
        self.assertEqual(user.verification_token.otp_submission_time, None)

    def test_response_for_incorrect_token(self):
        """
        This method tests that a http status code of 400 and an error message is
        returned if an incorrect One Time Password (OTP) is submitted by the user.
        """
        response = self.client.post(
            path=reverse('verify-email'),
            data={'verification_token': 154628}, # Invalid or incorrect token
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Token is incorrect.')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.is_verified, False)
        self.assertEqual(user.verification_token.is_used, False)

    def test_response_for_already_verified_email(self):
        """
        This method tests that a http status code of 400 and an error message is
        returned if a user that has already verified their email submits another
        otp for that purpose.
        """
        # Request to submit otp to verify email
        self.client.post(
            path=reverse('verify-email'),
            data=self.request_data,
            content_type='application/json'
        )

        user = User.objects.get(username='test_user')
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.verification_token.is_used, True)

        # Another request to receive otp for email verification by the same user.
        self.client.get(
            path=reverse('email-verification-token', kwargs={'user_id': user.id}),
        )

        # New otp
        user = User.objects.get(username='test_user')
        token = user.verification_token
        request_data2 = {'verification_token': token.verification_token}

        # Another request to verify email
        response2 = self.client.post(
            path=reverse('verify-email'),
            data=request_data2,
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.json().get('error'), 'Account has already been verified.')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.verification_token.is_used, False)

    def test_response_for_used_token(self):
        """
        This method tests that a http status code of 400 and error message is
        returned if a user tries to use an otp that has been used by another user
        to verify his/her provided email address.
        """
        # First user submits valid token and verifies email address.
        response1 = self.client.post(
            path=reverse('verify-email'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.json().get('message'), 'Email verified successfully.')

        # Second user makes a request and signs up successfully.
        data2 = {
            'username': 'test_user2',
            'email': 'test_user2@gmail.com',
            'password': 'password'
        }

        self.client.post(
            path=reverse('register-user'),
            data=data2,
            content_type='application/json'
        )

        # Second user tries to use same otp used by user one to verify
        # probably a fake email address, not knowing each generated token is tied
        # to a particular user, so will end up trying to verify the first user's
        # email address the second time.
        response2 = self.client.post(
            path=reverse('verify-email'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.json().get('error'), 'Token has been used.')

        user2 = User.objects.get(username='Test_user2')
        self.assertEqual(user2.is_verified, False)

    def test_response_for_expired_token(self):
        """
        This method tests that a http status code of 400 and error message is
        returned if a user submits a valid token after it has expired.
        """
        time.sleep(3)

        response = self.client.post(
            path=reverse('verify-email'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Token has expired.')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.is_verified, False)
        self.assertEqual(user.verification_token.is_used, False)

    def test_response_for_serializer_not_valid(self):
        """
        This method tests that a http status code of 400 and an error message
        is returned when the code block "serializer.is_valid()" fails to run.
        """
        del self.request_data['verification_token']

        response = self.client.post(
            path=reverse('verify-email'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['verification_token'][0], 'This field is required.')


class ValidatePasswordTokenTest(TestCase):
    """This class defines methods that tests ValidatePasswordResetTokenView class."""

    def setUp(self):
        """
        This method is called before the start of each method of the class
        and destroyed at the end of each method.
        """
        data = {
            'username': 'test_user',
            'email': 'test_user@gmail.com',
            'password': 'password'
        }

        self.client.post(
            path=reverse('register-user'),
            data=data,
            content_type='application/json'
        )

        request_body = {
            'email': 'test_user@gmail.com'
        }

        self.client.post(
            path=reverse('forgot-password-token'),
            data=request_body,
            content_type='application/json'
        )

        self.user = User.objects.get(username='Test_user')

        self.token = self.user.verification_token
        self.request_data = {'verification_token': self.token.verification_token}

        # Overide setting for time of expiration of otp
        settings.OTP_EXP_TIME = 2 # Two seconds

    def test_response_for_valid_token(self):
        """
        This method tests that a http status code of 200 and success messages are
        returned if a valid One Time Password (OTP) is submitted by the user. 
        """
        response = self.client.post(
            path=reverse('validate-password-reset-token'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'),
                         'Token for password reset verified successfully.')
        self.assertEqual(response.json().get('verification_token'), self.token.verification_token)

        user = User.objects.get(username='test_user')
        self.assertEqual(user.is_verified, False)
        self.assertEqual(user.verification_token.is_used, False)
        self.assertEqual(user.verification_token.is_for_password_reset, True)
        self.assertEqual(user.verification_token.is_validated_for_password_reset, True)
        self.assertEqual(type(user.verification_token.otp_submission_time), datetime)

    def test_response_for_incorrect_token(self):
        """
        This method tests that a http status code of 400 and an error message is
        returned if an incorrect One Time Password (OTP) is submitted by the user.
        """
        response = self.client.post(
            path=reverse('validate-password-reset-token'),
            data={'verification_token': 154628}, # Invalid or incorrect token,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Token is incorrect.')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.is_verified, False)
        self.assertEqual(user.verification_token.is_used, False)
        self.assertEqual(user.verification_token.is_for_password_reset, True)
        self.assertEqual(user.verification_token.is_validated_for_password_reset, False)
        self.assertEqual(type(user.verification_token.otp_submission_time), type(None))

    def test_response_for_used_token(self):
        """
        This method tests that a http status code of 400 and an error message is
        returned if a person tries to use an otp that has been used by a legit user
        to reset the legit user's password.
        """
        # First user submits valid token for password reset.
        self.client.post(
            path=reverse('validate-password-reset-token'),
            data=self.request_data,
            content_type='application/json'
        )

        # First user resets password.
        self.request_data['password'] = 'new_password'
        self.client.post(
            path=reverse('password-reset'),
            data=self.request_data,
            content_type='application/json'
        )

        user = User.objects.get(username='test_user')
        self.assertEqual(user.verification_token.is_used, True)
        self.assertTrue(user.password.startswith('argon2$argon2id$v=19$m=102400,t=2,p=8$'))
        self.assertTrue(user.check_password('new_password'))

        # Second person tries to use same otp used by user one to reset user1's password
        response = self.client.post(
            path=reverse('validate-password-reset-token'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Token has been used.')

    def test_response_for_expired_token(self):
        """
        This method tests that a http status code of 400 and error message is
        returned if a user submits a valid token after it has expired.
        """
        time.sleep(3)

        response = self.client.post(
            path=reverse('validate-password-reset-token'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Token has expired.')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.verification_token.is_for_password_reset, True)
        self.assertEqual(user.verification_token.is_used, False)
        self.assertEqual(user.verification_token.is_validated_for_password_reset, False)

    def test_response_for_serializer_not_valid(self):
        """
        This method tests that a http status code of 400 and an error message
        is returned when the code block "serializer.is_valid()" fails to run.
        """
        del self.request_data['verification_token']

        response = self.client.post(
            path=reverse('validate-password-reset-token'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['verification_token'][0], 'This field is required.')
