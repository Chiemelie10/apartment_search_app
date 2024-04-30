"""This module defines the endpoints related with the user app."""
from django.urls import path
from user.views.sign_up import SignUpView
from user.views.validate_token import (
    ValidateEmailVerificationTokenView,
    ValidatePasswordResetTokenView,
    ValidatePhoneVerificationOTP
)
from user.views.send_password_reset_email import SendPasswordResetToken
from user.views.send_verification_email import SendEmailVerificationToken
from user.views.password_reset import PasswordResetView
from user.views.login import LoginView
from user.views.logout import LogoutView
from user.views.token_refresh import CustomTokenRefreshView
from user.views.user_profile import UserProfileView
from user.views.get_users import UserView
from user.views.token_blacklist import CustomTokenBlacklistView
from user.views.send_phone_verification_otp import SendPhoneVerificationOTP


urlpatterns = [
    path('api/auth/register', SignUpView.as_view(), name='register_user'),
    path('api/send/email/verification-otp',
         SendEmailVerificationToken.as_view(), name='email_verification_token'),
    path('api/auth/email/verification-otp', ValidateEmailVerificationTokenView.as_view(),
         name='verify_email'),
    path('api/send/email/password-reset-otp', SendPasswordResetToken.as_view(),
         name='send_password_reset_token'),
    path('api/auth/email/password-reset-otp', ValidatePasswordResetTokenView.as_view(),
         name='validate_password_reset_token'),
    path('api/password-reset', PasswordResetView.as_view(), name='password_reset'),
    path('api/send/phone/verification-otp', SendPhoneVerificationOTP.as_view(),
         name='send_phone_verification_token'),
    path('api/auth/phone/verification-otp', ValidatePhoneVerificationOTP.as_view(),
         name='validate_phone_verification_token'),
    path('api/auth/login', LoginView.as_view(), name='login_user'),
    path('api/auth/logout', LogoutView.as_view(), name='logout_user'),
    path('api/users/blacklist', CustomTokenBlacklistView.as_view(), name='custom_token_blacklist'),
    path('api/token/refresh', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
    path('api/users', UserView.as_view(), name='get_users'),
    path('api/users/<str:user_id>/profile', UserProfileView.as_view(), name='user_profile'),
]
