from django.db import models
from live_chat_app.models import User

class Chat(models.Model):
    """
    Model representing a chat session.

    Attributes:
        user (ForeignKey): The user participating in the chat.
        admin (ForeignKey): The administrator participating in the chat.
        created_at (datetime): The date and time when the chat was created.
        last_message_timestamp (datetime): The date and time when the last message was sent in the chat.
        unread (bool): Indicates whether there are unread messages in the chat. Default is False.
        unread_count (int): The number of unread messages in the chat. Default is 0.
    """
    user = models.ForeignKey(User, related_name='chats', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, related_name='admin_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_timestamp = models.DateTimeField(null=True, blank=True)
    unread = models.BooleanField(default=False)
    unread_count = models.IntegerField(default=0)

    def __str__(self):
        return f'Chat between {self.user.email} and {self.admin.email}'
