"""This module defines the endpoints related with the user app."""
from django.urls import path
from user.views.sign_up import SignUpView
from user.views.validate_token import ValidateEmailVerificationTokenView
from user.views.validate_token import ValidatePasswordResetTokenView
from user.views.send_password_reset_email import SendPasswordResetToken
from user.views.send_verification_email import SendEmailVerificationToken
from user.views.password_reset import PasswordResetView


urlpatterns = [
    path('api/auth/register', SignUpView.as_view(), name='register-user'),
    path('api/users/<str:user_id>/mail/email-verification-token',
         SendEmailVerificationToken.as_view(), name='email-verification-token'),
    path('api/auth/email-verification-token', ValidateEmailVerificationTokenView.as_view(),
         name='verify-email'),
    path('api/mail/password-reset-token', SendPasswordResetToken.as_view(),
         name='forgot-password-token'),
    path('api/auth/password-reset-token', ValidatePasswordResetTokenView.as_view(),
         name='validate-password-reset-token'),
    path('api/password-reset', PasswordResetView.as_view(), name='password-reset'),
]
