"""This module defines class TokenBlacklistTest."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from user.serializers import TokenBlacklistSerializer
from user_suspension.models import UserSuspension


User = get_user_model()

class TokenBlacklistTest(TestCase):
    """This class defines methods that tests CustomTokenBlacklistView class."""
    def setUp(self):
        """
        This method is called before the start of each method of the class
        and destroyed at the end of each method.
        """
        # Data for the first user to be registered
        user1 = {
            'username': 'test_user',
            'email': 'test_user@gmail.com',
            'password': 'password'
        }

        # Data for the second user to be registered
        user2 = {
            'username': 'test_user2',
            'email': 'test_user2@gmail.com',
            'password': 'password'
        }

        # Register the first user
        self.client.post(
            path=reverse('register_user'),
            data=user1,
            content_type='application/json'
        )

        # Register the second user
        self.client.post(
            path=reverse('register_user'),
            data=user2,
            content_type='application/json'
        )

        # Login the first user
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
        self.user1 = User.objects.get(username='test_user')

    def test_resp_for_non_staff_users(self):
        """
        This method tests that users that are not staffs get a http 403 status code
        when they try to access the CustomTokenBlacklistView to suspend anothe user.
        """
        # Get the second user
        user2 = User.objects.get(username='test_user2')

        # Try to suspend the second user using non-staff first user
        response = self.client.post(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': 1
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Test response status code is equal to 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_resp_for_staff_users(self):
        """
        This method tests that a http status code of 200 is returned when a
        staff suspends another user.
        """
        # Make user1 a staff
        self.user1.is_staff = True
        self.user1.save()

        # Get the second user
        user2 = User.objects.get(username='test_user2')

        # Try to suspend the second user using the first user who has been made a staff.
        response = self.client.post(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': 1
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Test response status code is equal to 403
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'User has now been suspended.')

    def test_resp_for_has_ended_in_post_request(self):
        """
        This method tests that a http status code of 400 is returned when the
        "has_ended" field is set to True in the body of a post request.
        """
        # Make user1 a staff
        self.user1.is_staff = True
        self.user1.save()

        # Get the second user
        user2 = User.objects.get(username='test_user2')

        # Try to suspend the second user using the first user who has been made a staff.
        response = self.client.post(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': 1,
                'has_ended': True
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Test response status code is equal to 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resp_for_has_ended_in_patch_request(self):
        """
        This method tests that a http status code of 200 is returned when the
        "has_ended" field is set to True in the body of a patch request.
        """
        # Make user1 a staff
        self.user1.is_staff = True
        self.user1.save()

        # Get the second user
        user2 = User.objects.get(username='test_user2')

        # Request to suspend the second user.
        response1 = self.client.post(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': 1
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Test response status code is equal to 400
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.json().get('message'), 'User has now been suspended.')

        # Test that patch request to end the suspension of the second user with has_ended
        # set to true and duration/is_permanent in the body of the request will return a
        # http status code of 400.
        response2 = self.client.patch(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': 1,
                'has_ended': True
            },
            headers=self.headers,
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        # Test that request to suspend the second user with has_ended set to True and no
        # is_permanent or duration fields return http status code of 200.
        response3 = self.client.patch(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'has_ended': True
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Test response status code is equal to 400
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.json().get('message'), 'User has now been unsuspended.')

    def test_resp_for_previously_suspended_users(self):
        """
        This method tests that a http status code of 400 is returned when a user
        that had once been suspended is tried to be suspended again using post request.
        """
        # Make user1 a staff
        self.user1.is_staff = True
        self.user1.save()

        # Get the second user
        user2 = User.objects.get(username='test_user2')

        # Try to suspend the second user using the first user who has been made a staff.
        self.client.post(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': 1,
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Try to suspend the second user on second offence after the first suspension ended.
        response = self.client.post(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': None,
                'is_permanent': True
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Test response status code is equal to 405
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            response.json().get('error'), 'This account had once been suspended, '\
            'use the patch method to update the previously created suspension record.'
        )

    def test_get_suspension(self):
        """
        This method tests that all suspension data of the users
        currently and previously suspended are returned.
        """
        # pylint: disable=no-member

        # Make user1 a staff
        self.user1.is_staff = True
        self.user1.save()

        # Get all records of users currently and previously suspended.
        response = self.client.get(
            path=reverse('custom_token_blacklist'),
            headers=self.headers,
            content_type='application/json'
        )

        suspensions = UserSuspension.objects.all()
        serializer = TokenBlacklistSerializer(suspensions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.json())

    def test_success_resp_for_patch_method(self):
        """
        This method tests that the request using patch method returns
        a http status code of 200 on success.
        """
        # Make user1 a staff
        self.user1.is_staff = True
        self.user1.save()

        # Get the second user
        user2 = User.objects.get(username='test_user2')

        # Try to suspend the second user using the first user who has been made a staff.
        self.client.post(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': 1
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Try to update suspension record with patch method..
        response = self.client.patch(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': None,
                'is_permanent': True
            },
            headers=self.headers,
            content_type='application/json'
        )

        # Test response status code is equal to 403
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'User has now been suspended.')

    def test_patch_req_resp_for_users_not_prev_suspended(self):
        """
        This method tests that a http method of 400 is returned when patch
        method meant for update is used in attempt to suspend a user that has
        not been previously suspended. That is, the user had no record in the
        user_suspensions table before the request was made.
        """
         # Make user1 a staff
        self.user1.is_staff = True
        self.user1.save()

        # Get the second user
        user2 = User.objects.get(username='test_user2')

        # Try to suspend the second user for the first time using patch method.
        response = self.client.patch(
            path=reverse('custom_token_blacklist'),
            data={
                'user': user2.id,
                'duration': 1
            },
            headers=self.headers,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            response.json().get('error'), 'This account has not been suspended previously, '\
                'use post method to make the request.'
        )
