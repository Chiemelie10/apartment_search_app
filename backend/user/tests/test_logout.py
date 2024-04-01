"""This module defines class LogoutViewTest"""
import time
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

class LogoutViewTest(TestCase):
    """This class defines methods that tests LogoutView class."""
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

        # Login data
        response = self.client.post(
            path=reverse('login_user'),
            data={
                'username': 'test_user',
                'password': 'password'
            },
            content_type='application/json'
        )

        self.refresh_token = response.cookies['refresh'].value
        access_token = response.json().get('access')
        self.headers = {'Authorization': f'Bearer {access_token}'}

    def test_successful_logout(self):
        """
        This method tests that http status code of 204 is returned
        when there are no errors.
        """
        response = self.client.post(
            path=reverse('logout_user'),
            headers=self.headers,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(self.refresh_token, '')
        self.assertNotEqual(self.refresh_token, None)

        with self.assertRaises(TokenError) as context:
            RefreshToken(self.refresh_token).check_blacklist()

        self.assertEqual(str(context.exception), 'Token is blacklisted')

    def test_refresh_cookie_not_set(self):
        """
        This method tests that a http status code of 401 is returned when
        there is no refresh token cookie in the request.
        """
        response = self.client.post(
            path=reverse('logout_user'),
            headers=self.headers,
            HTTP_COOKIE='',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'),
                         'Refresh token must be set in the cookie.')

    def test_access_token_not_set_header(self):
        """
        This method tests that a http status code of 401 is returned when
        access token is not set in the header.
        """
        response = self.client.post(
            path=reverse('logout_user'),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('detail'),
                         'Authentication credentials were not provided.')

    def test_incorrect_refresh_token(self):
        """
        This method tests that a http status code of 401 is returned when
        refresh token is incorrect.
        """
        response = self.client.post(
            path=reverse('logout_user'),
            content_type='application/json',
            HTTP_COOKIE='refresh=incorrect.refresh.token',
            headers=self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'),
                         'Token is invalid or expired')

    def test_incorrect_access_token(self):
        """
        This method tests that a http status code of 401 is returned when
        access token is incorrect.
        """
        response = self.client.post(
            path=reverse('logout_user'),
            content_type='application/json',
            headers={'Authorization': 'Bearer incorrect.access.token'}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('messages')[0].get('message'),
                         'Token is invalid or expired')

    def test_expired_access_token(self):
        """
        This method tests that a http status code of 401 is returned when
        an expired access token is used.
        """
        time.sleep(3)

        response = self.client.post(
            path=reverse('logout_user'),
            content_type='application/json',
            headers=self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('messages')[0].get('message'),
                         'Token is invalid or expired')
