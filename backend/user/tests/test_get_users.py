"""This method defines class GetUsersTest."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.request import Request
from user.serializers import UserSerializer


User = get_user_model()

class GetUsersTest(TestCase):
    """This class defines methods that tests UserView."""

    def setUp(self):
        """
        This method is called before the start of each method of the class
        and destroyed at the end of each method.
        """
        # Data for the user to be registered
        user = {
            'username': 'test_user',
            'email': 'test_user@gmail.com',
            'password': 'password'
        }

        # Register the user
        self.client.post(
            path=reverse('register_user'),
            data=user,
            content_type='application/json'
        )

        # Login the user
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

    def test_resp_if_user_not_staff(self):
        """
        This method tests that a http status code of 403 is returned if user
        accessing the UserView is not a staff.
        """
        response = self.client.get(
            path=reverse('get_users'),
            headers=self.headers,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get('detail'), 'You do not have permission to perform this action.'
        )

    def test_resp_if_user_is_staff(self):
        """
        This method tests that a http status code of 200 is returned if user
        accessing the UserView is a staff.
        """
        # Log user out
        self.client.post(
            path=reverse('logout_user'),
            headers=self.headers
        )

        # Make the user a staff
        self.user.is_staff = True
        self.user.save()

        # Login user that is now a staff
        response = self.client.post(
            path=reverse('login_user'),
            data={
                'username': 'test_user',
                'password': 'password'
            },
            content_type='application/json'
        )

        # Get access token from response
        access_token = response.json().get('access')
        headers = {'Authorization': f'Bearer {access_token}'}

        # Test response for request to get all users
        response2 = self.client.get(
            path=reverse('get_users'),
            headers=headers,
            content_type='application/json'
        )

        request = Request(response2.wsgi_request)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response2.json())
