from rest_framework import serializers
from live_chat_app.models import Message, User, Chat
from live_chat_app.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    Converts the Message model instances to JSON format and vice versa.
    """
    user_email = serializers.EmailField(write_only=True)
    chat_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat_id', 'user_email', 'user', 'text', 'created_at']

    def create(self, validated_data):
        chat_id = validated_data.pop('chat_id')
        user_email = validated_data.pop('user_email')
        
        # Retrieve chat and user instances
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(email=user_email)
        
        # Create a new message
        message = Message.objects.create(chat=chat, user=user, **validated_data)
        return message
