"""This module defines class User"""
from uuid import uuid4
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from user_role.models import UserRole
from user_interest.models import UserInterest


class CustomUserManager(BaseUserManager):
    """This class defines createuser and createsuperuser methods."""
    def create_user(self, username, email, password, **other_fields):
        """This method creates a new user."""
        if not username:
            raise ValueError('Username is required.')
        if not email:
            raise ValueError('Email is required.')
        if not password:
            raise ValueError('Password is required.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, password=password, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **other_fields):
        """This method creates a superuser user."""
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff set to true.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser set to true.')
        return self.create_user(username, email, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """This class defines the attributes of a user within the application."""
    id = models.CharField(default=uuid4, max_length=36,
                        unique=True, primary_key=True, editable=False)
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, editable=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'users'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        return f'{self.id} {self.username}'

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female')
)

class UserProfile(models.Model):
    """This class defines the additional fields need for a complete user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                primary_key=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name='profiles',
                             blank=True, null=True)
    interests = models.ManyToManyField(UserInterest, through='UserProfileInterest')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=14, null=True, blank=True,
                                    validators=[MinLengthValidator(limit_value=11)])
    thumbnail = models.ImageField(upload_to='thumbnail', blank=True, null=True)

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'user_profiles'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'{self.user.id} {self.user.username}'


class UserProfileInterest(models.Model):
    """
    This class defines the fields of the junction table between
    user_profiles table and user_interests table.
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_interest = models.ForeignKey(UserInterest, on_delete=models.CASCADE)

    class Meta:
        """ db_table: Name of the table this class creates in the database."""
        db_table = 'user_profile_interests'

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'Username: {self.user_profile.user.username} - Interest: {self.user_interest.name}'
