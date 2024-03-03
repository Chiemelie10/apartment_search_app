"""This module defines class PasswordResetViewTest"""
import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()

class PasswordResetViewTest(TestCase):
    """This class defines methods that tests PasswordResetView class."""

    def setUp(self):
        """
        This method is called before the start of each method of the class
        and destroyed at the end of each method.
        """
        # Data for a user to be registered
        data = {
            'username': 'test_user',
            'email': 'test_user@gmail.com',
            'password': 'password'
        }

        # Register the user
        self.client.post(
            path=reverse('register_user'),
            data=data,
            content_type='application/json'
        )

        # Data for password reset.
        request_body = {
            'email': 'test_user@gmail.com'
        }

        # Request to get otp for password reset.
        self.client.post(
            path=reverse('forgot_password_token'),
            data=request_body,
            content_type='application/json'
        )

        # Get otp sent to the user called token
        self.user = User.objects.get(username='Test_user')

        self.token = self.user.verification_token
        self.request_data = {'verification_token': self.token.verification_token}

        # Request to validate token
        # Note access token cookie will be set automatically after this request.
        response = self.client.post(
            path=reverse('validate_password_reset_token'),
            data=self.request_data,
            content_type='application/json'
        )

        self.access_token = response.cookies['access'].value

        # new password to be set
        self.request_data['password'] = 'new_password'

    def test_response_for_valid_access_token(self):
        """
        This method tests that a http status code of 200 and a success message is
        returned if a valid One Time Password (OTP) is submitted by the user. 
        """
        # Request to reset password
        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Password reset was successful.')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.verification_token.is_used, True)
        self.assertEqual(user.verification_token.is_for_password_reset, True)
        self.assertEqual(user.verification_token.is_validated_for_password_reset, True)
        # Check access token cookie was deleted after request
        self.assertEqual(response.cookies['access'].value, '')

    def test_response_for_incorrect_access_token(self):
        """
        This method tests that a http 400 status code and error message are
        returned if an incorrect One Time Password (OTP) is submitted by the user.
        """
        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            HTTP_COOKIE='access=incorrect.access.token', # Override access token cookie
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'), 'Token is invalid or expired')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.verification_token.is_used, False)
        self.assertEqual(user.verification_token.is_for_password_reset, True)
        self.assertEqual(user.verification_token.is_validated_for_password_reset, True)

    def test_response_for_same_access_token(self):
        """
        This method tests that a http status code of 400 and an error message is
        returned if a person tries to use same access token that has been used by
        a legit user to reset the legit user's password.
        """
        # First user resets password.
        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            content_type='application/json'
        )

        user = User.objects.get(username='test_user')
        self.assertEqual(user.verification_token.is_used, True)
        self.assertEqual(response.cookies['access'].value, '')

        # Second person tries to use same token used by user one to reset user1's password
        self.request_data['password'] = 'hacked_password'
        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            HTTP_COOKIE=f'access={self.access_token}', # Stolen user1 token added to request
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Token has been used.')

    def test_response_for_is_for_password_reset(self):
        """
        This method tests that a http status code of 401 and an error message is returned
        if a user tries to use an otp that was not generated for password reset to reset
        his/her password.
        """
        user = User.objects.get(username='test_user')
        user.verification_token.is_for_password_reset = False
        user.verification_token.save()

        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'),
                         'You are not permitted to use this resource.')

    def test_response_for_is_validated_for_password_reset(self):
        """
        This method tests that a http status code of 401 and an error message is returned
        if a user tries to use an otp that has not been validated to reset his/her password.
        """
        user = User.objects.get(username='test_user')
        user.verification_token.is_validated_for_password_reset = False
        user.verification_token.save()

        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'),
                         'You are not permitted to use this resource.')

    def test_response_for_expired_token(self):
        """
        This method tests that a http status code of 401 and an error message is
        returned if a user submits form for password reset after access token has
        expired.
        """
        time.sleep(3)

        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'), 'Token is invalid or expired')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.verification_token.is_for_password_reset, True)
        self.assertEqual(user.verification_token.is_used, False)
        self.assertEqual(user.verification_token.is_validated_for_password_reset, True)

    def test_response_for_cookie_not_set(self):
        """
        This method tests that a http status code of 401 and an error message is
        returned if a user submits form for password reset without access token
        cookie set.
        """
        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            HTTP_COOKIE='',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'),
                         'Access token must be set in the cookie.')

        user = User.objects.get(username='test_user')
        self.assertEqual(user.verification_token.is_for_password_reset, True)
        self.assertEqual(user.verification_token.is_used, False)
        self.assertEqual(user.verification_token.is_validated_for_password_reset, True)

    def test_response_for_no_password_in_request_body(self):
        """
        This method tests that a http status code of 400 and an error message
        is returned if the code block "serializer.is_valid()" fails to run, due
        to request body having no password.
        """
        del self.request_data['password']

        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password'][0], 'This field is required.')

    def test_response_for_invalid_password(self):
        """
        This method tests that a http status code of 400 and an error message
        is returned if the code block "serializer.is_valid()" fails to run, due
        to the value of the submitted password not meeting with one or more of the
        validation requirements.
        """
        self.request_data['password'] = 'new'

        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password'][0],
                         'This password is too short. It must contain at least 8 characters.')

    def test_hash_password(self):
        """
        This method tests that the new password set by the user after
        password reset is saved in the database and hashed.
        """
        response = self.client.post(
            path=reverse('password_reset'),
            data=self.request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Password reset was successful.')

        user = User.objects.get(username='test_user')
        self.assertTrue(user.password.startswith('argon2$argon2id$v=19$m=102400,t=2,p=8$'))
        self.assertTrue(user.check_password('new_password'))
        self.assertEqual(len(user.password), 112)
