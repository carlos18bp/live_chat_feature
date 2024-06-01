from django.db import models
from live_chat_app.models import User
from live_chat_app.models import Chat

class Message(models.Model):
    """
    Model representing a chat message.

    Attributes:
        chat (ForeignKey): The chat this message belongs to.
        user (ForeignKey): The user who sent the message.
        text (str): The content of the message.
        created_at (datetime): The date and time when the message was created.
    """
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.user.email} at {self.created_at}'
