"""This module defines class TokenRefreshTest"""
import time
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

class TokenRefreshTest(TestCase):
    """This class defines methods that tests CustomTokenRefreshView class."""

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

    def test_successful_refresh(self):
        """
        This method tests that refresh token is set in the cookie while access token
        is returned in the body of the response if a valid refresh token is set in the
        cookie for the request.
        """
        response = self.client.post(
            path=reverse('custom_token_refresh'),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.json().get('access')
        access_token = AccessToken(token)
        self.assertEqual(access_token.get('token_type'), 'access')

        token = response.cookies['refresh'].value
        refresh_token = RefreshToken(token)
        self.assertEqual(refresh_token.get('token_type'), 'refresh')

    def test_refresh_token_not_set(self):
        """
        This method tests that a status code of 401 is returned when
        refresh token is not set in the cookie.
        """
        response = self.client.post(
            path=reverse('custom_token_refresh'),
            content_type='application/json',
            HTTP_COOKIE=''
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'),
                         'Refresh token must be set in the cookie.')

    def test_expired_refresh_token(self):
        """
        This method tests that a status code of 401 is returned when
        refresh token set in the cookie has expired.
        """
        time.sleep(6)

        response = self.client.post(
            path=reverse('custom_token_refresh'),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'), 'Token is invalid or expired')

    def test_token_blacklist_on_refresh(self):
        """This method tests that a refresh token is blacklisted after refresh."""
        response = self.client.post(
            path=reverse('custom_token_refresh'),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(TokenError) as context:
            RefreshToken(self.refresh_token)

        self.assertEqual(str(context.exception), 'Token is blacklisted')

    def test_blacklist_outstanding_token(self):
        """
        This method tests that all refresh tokens beloging to a
        user is blacklisted after a person make a request with a
        blacklisted token.
        """
        # pylint: disable=no-member

        user = User.objects.get(username='Test_user')

        #  Other login by the user
        for _ in range(0, 3):
            RefreshToken.for_user(user)


        response = self.client.post(
            path=reverse('custom_token_refresh'),
            content_type='application/json',
            HTTP_COOKIE=f'refresh={self.refresh_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_tokens = OutstandingToken.objects.filter(user=user)
        self.assertEqual(len(refresh_tokens), 5)
        blacklisted_tokens = BlacklistedToken.objects.all()
        self.assertEqual(len(blacklisted_tokens), 1)

        response2 = self.client.post(
            path=reverse('custom_token_refresh'),
            content_type='application/json',
            HTTP_COOKIE=f'refresh={self.refresh_token}'
        )

        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response2.json().get('error'), 'Token is blacklisted')

        blacklisted_tokens = BlacklistedToken.objects.all()
        self.assertEqual(len(blacklisted_tokens), 5)
