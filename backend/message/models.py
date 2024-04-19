"""This module defines class Message."""
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Message(models.Model):
    """This class defines the fields of the messages table in the database."""
    id = models.CharField(default=uuid4, max_length=36,
                          unique=True, primary_key=True, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='message_images', null=True, blank=True)
    parent_message = models.ForeignKey('self', related_name='replies',
                                       null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        db_table: Name of the table this class creates in the database.
        ordering: The order the instances of this model is displayed on the admin page.
        """
        db_table = 'messages'
        ordering = ['-created_at']

    def __str__(self):
        """This method returns a string representation of the instance of this class."""
        # pylint: disable=no-member
        return f'message_id: {self.id} - sent by: {self.sender.username} '\
               f'- sent to: {self.receiver.username}'
