from rest_framework import serializers
from live_chat_app.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Converts the User model instances to JSON format and vice versa.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_admin']
