"""This module defines class UserModelTest"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from user.models import UserProfile


User = get_user_model()

class UserModelTest(TestCase):
    """This class defines methods that tests key aspects of the User model"""

    def setUp(self):
        """This method is called before each test method in the class."""
        self.user = User.objects.create_user(
            username="test_user",
            email="testuser@gmail.com",
            password="test_user_password"
        )

    def test_password_hash(self):
        """
        This method tests that the user's password saved in the database is hashed
        when "create_user" method is used to create a new user.
        """
        user = User.objects.get(username='test_user')
        self.assertTrue(user.password.startswith('argon2$argon2id$v=19$m=102400,t=2,p=8$'))
        self.assertEqual(len(user.password), 112)
        self.assertTrue(user.check_password('test_user_password'))

    def test_password_not_set(self):
        """
        This method tests that a ValueError exception is raised when the value for password was
        not passed into the "create_user" method.
        """
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                username="test_user_two",
                email="test_user_two@gmail.com",
                password=""
            )

        self.assertEqual('Password is required.', str(context.exception))

    def test_unique_username(self):
        """
        This method confirms an exception is raised in the username field
        of the User model, when a username that already exists in the database
        is used to register a new user via the "create_user" method.
        """
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="test_user",
                email="anotheremail@gmail.com",
                password="password"
            )

    def test_username_not_set(self):
        """
        This method tests that a ValueError exception is raised when the value for username was
        not passed into the "create_user" method.
        """
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email="test_user_two@gmail.com",
                password="password",
                username=""
            )

        self.assertEqual('Username is required.', str(context.exception))

    def test_unique_email(self):
        """
        This method confirms an exception is raised in the email field
        of the User model, when an email that already exists in the database
        is used to register a new user via the "create_user" method.
        """
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="another_user",
                email="testuser@gmail.com",
                password="password"
            )

    def test_email_not_set(self):
        """
        This method tests that a ValueError exception is raised when the value for email was
        not passed into the "create_user" method.
        """
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                username="test_user_two",
                password="password",
                email=""
            )

        self.assertEqual('Email is required.', str(context.exception))

    def test_create_user_boolean_fields(self):
        """
        This method tests that the boolean fields store the right
        default values when "create_user" method is used.
        """
        user = User.objects.get(username='test_user')

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_verified)
        self.assertTrue(user.is_active)

    def test_create_superuser_boolean_fields(self):
        """
        This method tests that the boolean fields store the right
        default values when "create_user" method is used.
        """
        user = User.objects.create_superuser(
            username='test_superuser',
            password='password',
            email="testsuperuser@gmail.com"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.is_verified)
        self.assertTrue(user.is_active)

    def test_user_model_str_method(self):
        """
        This method tests if user object has equal value with
        the string returned in the __str__ method of the User model.
        """
        user = User.objects.get(username="test_user")
        self.assertEqual(f'{user.id} {user.username}', str(user))

    def test_userprofile_model_str_method(self):
        """
        This method tests if user object has equal value with
        the string returned in the __str__ method of the User model.
        """
        # pylint: disable=no-member

        user = User.objects.get(username="test_user")
        user_profile = UserProfile.objects.create(user=user, phone_number='07058679688')
        self.assertEqual(f'{user.id} {user.username}', str(user_profile))
