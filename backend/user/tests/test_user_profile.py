"""This module defines class UserProfileTest."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from user_suspension.models import UserSuspension
from user.serializers import UserSerializer
from user_role.models import UserRole
from user_interest.models import UserInterest


User = get_user_model()

class UserProfileTest(TestCase):
    """This class defines methods that tests UserProfileView."""
    def setUp(self):
        """
        This method is called before the start of each method of the class
        and destroyed at the end of each method.
        """
        # Data for the first user to be registered
        user1 = {
            'username': 'test_user1',
            'email': 'test_user1@gmail.com',
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
        response_user1 = self.client.post(
            path=reverse('login_user'),
            data={
                'username': 'test_user1',
                'password': 'password'
            },
            content_type='application/json'
        )

        # Get access token for user1
        self.access_token_user1 = response_user1.json().get('access')
        self.headers_user1 = {'Authorization': f'Bearer {self.access_token_user1}'}
        self.user1 = User.objects.get(username='test_user1')

        # Login the second user
        response_user2 = self.client.post(
            path=reverse('login_user'),
            data={
                'username': 'test_user2',
                'password': 'password'
            },
            content_type='application/json'
        )

        # Get access token for user2
        self.access_token_user2 = response_user2.json().get('access')
        self.headers_user2 = {'Authorization': f'Bearer {self.access_token_user2}'}
        self.user2 = User.objects.get(username='test_user2')

    def test_get_user_profile_by_user(self):
        """
        This method tests the a http status code of 200 is returned when
        a user makes get request to view their profile.
        It also tests some of the key and value pairs in the json response returned. 
        """
        # Test response if user_id correct
        response = self.client.get(
            path=reverse('user_profile', kwargs={'user_id': self.user1.id}),
            headers=self.headers_user1
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.json())

        # Test response if user_id is incorrect
        response = self.client.get(
            path=reverse('user_profile', kwargs={'user_id': 'incorrect_id'}),
            headers=self.headers_user1
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('error'), 'User not found.')

    def test_get_user_profile_by_another_user(self):
        """
        This method tests the a http status code of 200 is returned when
        a user makes get request to view another user's profile.
        It also tests some of the key and value pairs in the json response returned. 
        """
        # pylint: disable=no-member

        # Test response if user_id correct
        response = self.client.get(
            path=reverse('user_profile', kwargs={'user_id': self.user2.id}),
            headers=self.headers_user1
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('email', response.json())

        # Test response if user_id is incorrect
        response = self.client.get(
            path=reverse('user_profile', kwargs={'user_id': 'incorrect_id'}),
            headers=self.headers_user1
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('error'), 'User not found.')

        # Suspend user2 permanently
        UserSuspension.objects.create(
            user=self.user2,
            is_permanent=True,
            duration=None,
            start_time=timezone.now(),
            end_time=None,
            number_of_suspensions=1
        )

        # Set is_active attribute of the user to False after suspendin the user
        self.user2.is_active = False
        self.user2.save()

        # Test response when the user that owns the profile is suspended.
        response = self.client.get(
            path=reverse('user_profile', kwargs={'user_id': self.user2.id}),
            headers=self.headers_user1
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get('error'), 'This account is suspended.')

    def test_put_and_patch_method(self):
        """
        This method tests the conditions stated in the put and patch
        methods of the UserProfileView.
        """
        # pylint: disable=no-member

        # Create user roles
        UserRole.objects.create(name='agent')
        UserRole.objects.create(name='student')

        # Create user interest
        UserInterest.objects.create(name='christian')
        UserInterest.objects.create(name='muslim')
        UserInterest.objects.create(name='non-smoker')

        # Data to be updated for user2
        user2_data = {
            'phone_number': '07058679688',
            'gender': 'male',
            'role': 1,
            'first_name': 'Eze',
            'last_name': 'Chiemelie',
            'thumbnail': None,
            'interests': [
                {
                    'user_interest': 1
                },
                {
                    'user_interest': 2
                },
            ],
        }

        # Put method test starts here
        # Test response if a user tries to update another user's profile
        response = self.client.put(
            path=reverse('user_profile', kwargs={'user_id': self.user2.id}),
            data=user2_data,
            headers=self.headers_user1,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get('error'), 'Profile can only be updated by the owner.'
        )

        # Test response if a user tries to update his/her profile.
        response = self.client.put(
            path=reverse('user_profile', kwargs={'user_id': self.user2.id}),
            data=user2_data,
            headers=self.headers_user2,
            content_type='application/json'
        )

        request = Request(response.wsgi_request)
        user = User.objects.get(username='test_user2')
        serializer = UserSerializer(user, context={'request': request})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

        # Patch method test starts here.
        # Test response if a user tries to update another user's profile
        response = self.client.patch(
            path=reverse('user_profile', kwargs={'user_id': self.user2.id}),
            data=user2_data,
            headers=self.headers_user1,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get('error'), 'Profile can only be updated by the owner.'
        )

        # User2 partly updates his/her profile using patch method.
        response = self.client.patch(
            path=reverse('user_profile', kwargs={'user_id': self.user2.id}),
            data= {
                'role': 2,
                'first_name': 'Ezeh',
                'email': 'test_user3@gmail.com',
                'interests': [
                    {
                        'user_interest': 1
                    },
                    {
                        'user_interest': 3
                    }
                ]
            },
            headers=self.headers_user2,
            content_type='application/json'
        )

        request = Request(response.wsgi_request)
        user = User.objects.get(username='test_user2')
        serializer = UserSerializer(user, context={'request': request})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_delete_method(self):
        """This method tests the conditions stated in the delete method of the UserProfileView."""
        # Test response when a user tries to delete another user's account.
        response = self.client.delete(
            path=reverse('user_profile', kwargs={'user_id': self.user2.id}),
            headers=self.headers_user1,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get('error'), 'Account can only be deleted by the owner.'
        )

        # Test response when a user tries to delete his/her own account.
        response = self.client.delete(
            path=reverse('user_profile', kwargs={'user_id': self.user2.id}),
            headers=self.headers_user2,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Account deleted successfully.')
