"""This module defines the endpoints related with the apartment app."""
from django.urls import path
from message.views.create_message import CreateMessageView
from message.views.get_messages import GetUserMessagesView
from message.views.get_user_to_user_messages import GetUserToUserMessages


urlpatterns = [
    path('api/messages/create', CreateMessageView.as_view(), name='create_message'),
    path('api/messages/<str:user_id>', GetUserMessagesView.as_view(), name='get_user_messages'),
    path('api/messages/<str:user_id>/<str:user2_id>', GetUserToUserMessages.as_view(),
         name='get_user_to_user_messages'),
]
