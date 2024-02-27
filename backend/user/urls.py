"""This module defines the endpoints related with the user app."""
from rest_framework_simplejwt.views import TokenBlacklistView
from django.urls import path
from user.views.sign_up import SignUpView
from user.views.validate_token import ValidateEmailVerificationTokenView
from user.views.validate_token import ValidatePasswordResetTokenView
from user.views.send_password_reset_email import SendPasswordResetToken
from user.views.send_verification_email import SendEmailVerificationToken
from user.views.password_reset import PasswordResetView
from user.views.login import LoginView
from user.views.logout import LogoutView
from user.views.token_refresh import CustomTokenRefreshView


urlpatterns = [
    path('api/auth/register', SignUpView.as_view(), name='register_user'),
    path('api/users/<str:user_id>/mail/email-verification-token',
         SendEmailVerificationToken.as_view(), name='email_verification_token'),
    path('api/auth/email-verification-token', ValidateEmailVerificationTokenView.as_view(),
         name='verify_email'),
    path('api/mail/password-reset-token', SendPasswordResetToken.as_view(),
         name='forgot_password_token'),
    path('api/auth/password-reset-token', ValidatePasswordResetTokenView.as_view(),
         name='validate_password_reset_token'),
    path('api/password-reset', PasswordResetView.as_view(), name='password_reset'),
    path('api/auth/login', LoginView.as_view(), name='login_user'),
    path('api/auth/logout', LogoutView.as_view(), name='logout_user'),
    path('api/token/blacklist', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/token/refresh', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
]
