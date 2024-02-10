"""This module defines the endpoints related with the user app."""
from django.urls import path
from user.views.sign_up import SignUpView
from user.views.verify_email import VerifyEmail
from user.views.send_verification_email import SendEmailVerificationLink


urlpatterns = [
    path('api/auth/register/', SignUpView.as_view(), name='register-user'),
    path('api/activate-account/<str:user_id>/', VerifyEmail.as_view(), name='activate-account'),
    path('api/send-verification-email/<str:user_id>/', SendEmailVerificationLink.as_view(),
         name='send-verification-email'),
]
