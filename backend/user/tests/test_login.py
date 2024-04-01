"""This module defines class LoginViewTest"""
import time
from datetime import timedelta
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from user_suspension.models import UserSuspension


User = get_user_model()

class LoginViewTest(TestCase):
    """This class defines methods that tests LoginViewTest class."""
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
        self.login_data = {
            'username': 'test_user',
            'password': 'password'
        }

    def test_login_with_username(self):
        """This method tests that a user can login with username."""
        response = self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('message'), 'User login was successful.')
        self.assertNotEqual(response_data.get('access'), None)
        self.assertEqual(response.cookies['refresh'].key, 'refresh')
        self.assertNotEqual(response.cookies['refresh'].value, '')
        self.assertNotEqual(response.cookies['refresh'].value, None)

    def test_login_with_email(self):
        """This method tests that a user can login with email."""
        self.login_data = {
            'email': 'test_user@gmail.com',
            'password': 'password'
        }

        response = self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('message'), 'User login was successful.')
        self.assertNotEqual(response_data.get('access'), None)
        self.assertEqual(response.cookies['refresh'].key, 'refresh')
        self.assertNotEqual(response.cookies['refresh'].value, '')
        self.assertNotEqual(response.cookies['refresh'].value, None)

    def test_incorrect_username(self):
        """
        This methods tests that a http 404 error is returned when a user
        tries to login with incorrect username.
        """
        # Login with wrong username
        self.login_data = {
            'username': 'incorrect_username',
            'password': 'password'
        }

        response = self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data.get('error'), 'User not found.')
        self.assertEqual(response_data.get('access'), None)

        with self.assertRaises(KeyError):
            self.assertEqual(response.cookies['refresh'].key, '')

    def test_incorrect_email(self):
        """
        This methods tests that a http 404 error is returned when a user
        tries to login with incorrect email.
        """
        # Login with wrong email
        self.login_data = {
            'username': 'incorrectemail@gmail.com',
            'password': 'password'
        }

        response = self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data.get('error'), 'User not found.')
        self.assertEqual(response_data.get('access'), None)

        with self.assertRaises(KeyError):
            self.assertEqual(response.cookies['refresh'].key, '')

    def test_incorrect_password(self):
        """
        This methods tests that a http 404 error is returned when a user
        tries to login with incorrect password.
        """
        # Login with wrong email
        self.login_data['password'] = 'inccorrect_password'

        response = self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data.get('error'), 'User not found.')
        self.assertEqual(response_data.get('access'), None)

        with self.assertRaises(KeyError):
            self.assertEqual(response.cookies['refresh'].key, '')

    def test_blacklist_outstanding_tokens(self):
        """
        This method checks that all outstanding refresh tokens of a user are
        blacklisted before the user gets a new refresh token in the login view.
        """
        # pylint: disable=no-member

        for _ in range(0, 3):
            self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )

        user = User.objects.get(username='test_user')
        outstanding_tokens = OutstandingToken.objects.filter(user=user)
        self.assertEqual(len(outstanding_tokens), 3)

        blacklisted_token = BlacklistedToken.objects.all()
        self.assertEqual(len(blacklisted_token), 2)

    def test_suspended_user_login_response(self):
        """
        This method tests that that suspended users are unable to login.
        It also tests the users are able to login after their suspension ends.
        """
        # pylint: disable=no-member

        # Get user
        user = User.objects.get(username='test_user')

        # Suspend user permanently
        UserSuspension.objects.create(
            user=user,
            is_permanent=True,
            duration=None,
            start_time=timezone.now(),
            end_time=None,
            number_of_suspensions=1
        )

        # Set is_active attribute of the user to False after suspendin the user
        user.is_active = False
        user.save()

        # Test response after user tries to login
        response = self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )

        self.assertEqual(response.json().get('error'), 'Account has been permanently suspended.')

        # User is suspended for 2 seconds
        user.suspension.is_permanent = False
        user.suspension.duration = 1
        user.suspension.start_time = timezone.now()
        user.suspension.end_time = timezone.now() + timedelta(seconds=2)
        user.suspension.number_of_suspensions = 2
        user.suspension.save()

        # Test response after user tries to login before 2 seconds expires.
        response = self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )
        self.assertEqual(response.json().get('error'), 'Account was suspended, '\
                         'time remaining is a second.')

        # 3 seconds passes
        time.sleep(3)

        # Test response after user tries to login after 2 seconds passes.
        response = self.client.post(
            path=reverse('login_user'),
            data=self.login_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'User login was successful.')

        # Test user is_active attribute after login
        user = User.objects.get(username='test_user')
        self.assertEqual(user.is_active, True)
