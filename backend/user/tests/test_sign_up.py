"""This module defines class SignUpViewTest"""
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer


User = get_user_model()

class SignUpViewTest(TestCase):
    """This class defines methods that test the functionality of the SignUp View."""

    def setUp(self):
        """
        This method is called before the start of each method of the class.
        """
        self.data = {
            "username": "test_user",
            "email": "test_user@gmail.com",
            "password": "password"
        }

    def test_serializer_is_valid(self):
        """
        This method tests that a the view successfully creates
        a user and save to the database if serializer.is_valid() runs.
        """
        response = self.client.post(
            path=reverse('register_user'),
            data=self.data,
            content_type="application/json"
        )

        user = User.objects.get(username="test_user")
        serializer = UserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), serializer.data)

    def test_serializer_not_valid(self):
        """
        This method tests that a the view returns a 400 http status code
        and list of error messages if serializer.is_valid() did not run.
        """
        data = self.data
        del data['username']
        data['password'] = '<script>password<script>'

        response = self.client.post(
            path=reverse('register_user'),
            data=data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(response_data['username'][0], 'This field is required.')
        self.assertEqual(response_data['password'][0],
                         'html tags or anything similar is not allowed.')

    def test_content_type(self):
        """
        This method tests that a 400 http status code and error message is returned
        if Content-Type is not set to application/json in the header of the request.
        """
        response = self.client.post(
            path=reverse('register_user'),
            data=self.data,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(response_data.get('error'),
                         'Content-Type must be application/json.')

    def test_user_model_default_values(self):
        """
        This method tests that the default values given in the User model
        will remain unchanged, even when a new value is provided for any of
        those fields in the sign up view.
        """
        data = self.data
        data['is_superuser'] = True
        data['is_staff'] = True
        data['is_verified'] = True
        data['is_active'] = False

        response = self.client.post(
            path=reverse('register_user'),
            data=data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertFalse(response_data.get('is_superuser'))
        self.assertFalse(response_data.get('is_staff'))
        self.assertFalse(response_data.get('is_verified'))
        self.assertTrue(response_data.get('is_active'))

    def test_password_hash(self):
        """
        This method tests that the password saved in the database
        for the created user is hashed.
        """
        response = self.client.post(
            path=reverse('register_user'),
            data=self.data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='test_user')
        self.assertTrue(user.password.startswith('argon2$argon2id$v=19$m=102400,t=2,p=8$'))
        self.assertEqual(len(user.password), 112)
        self.assertTrue(user.check_password('password'))

    def test_unique_username(self):
        """
        This method tests that a http 400 status code and error message are
        returned when the a username that already exists in the database is used
        in the body of the request.
        """
        self.client.post(
            path=reverse('register_user'),
            data=self.data,
            content_type="application/json"
        )

        self.data['email'] = 'test_user2@gmail.com'

        response = self.client.post(
            path=reverse('register_user'),
            data=self.data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['username'][0],
                         'user with this username already exists.')

    def test_unique_email(self):
        """
        This method tests that a http 400 status code and error message are
        returned when the an email address that already exists in the database
        is used in the body of the request.
        """
        self.client.post(
            path=reverse('register_user'),
            data=self.data,
            content_type="application/json"
        )

        self.data['username'] = 'test_user2'

        response = self.client.post(
            path=reverse('register_user'),
            data=self.data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'][0],
                         'user with this email already exists.')
