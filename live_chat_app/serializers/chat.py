from rest_framework import serializers
from live_chat_app.models import Chat
from live_chat_app.serializers import UserSerializer, MessageSerializer

class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Chat model.

    Converts the Chat model instances to JSON format and vice versa.
    """
    user = UserSerializer()
    admin = UserSerializer()
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['id', 'user', 'admin', 'messages', 'last_message_timestamp', 'unread', 'unread_count']
