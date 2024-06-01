import json
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from live_chat_app.models import User, Message, Chat
from live_chat_app.serializers import UserSerializer, MessageSerializer, ChatSerializer

@api_view(['POST'])
def admin_get_or_create(request):
    """
    View to get an existing user admin by email or create a new one if it doesn't exist.

    POST:
        Validate if the admin user exists by email. If not, create the admin user.
    """
    try:
        admin, created = User.objects.get_or_create(email="admin@example.com", defaults={'first_name': "Admin", 'last_name': "Web Site", 'is_admin': 'True'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(admin)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_get_or_create(request):
    """
    View to create a new user or get an existing user by email.

    POST:
        Validate if the user exists by email. If not, create a new user.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email or not first_name or not last_name:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user, created = User.objects.get_or_create(
            email=email, defaults={'first_name': first_name, 'last_name': last_name}
        )
        serializer = UserSerializer(user)
        if not created:
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def chat_list_create(request):
    """
    View to list all chats or create a new chat.

    GET:
        List all chats.
    POST:
        Create a new chat. Send an email notification when a new chat is created.
    """
    if request.method == 'GET':
        chats = Chat.objects.all().order_by('-created_at')
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

        user_email = data['user_email']
        admin_email = data['admin_email']

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            admin = User.objects.get(email=admin_email)
        except User.DoesNotExist:
            return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the chat between user and admin already exists
        chat, created = Chat.objects.get_or_create(user=user, admin=admin)

        if created:
            # Add a default welcome message
            welcome_message = Message.objects.create(
                chat=chat,
                user=admin,
                text="This is a default welcome message",
                created_at=timezone.now()
            )
            chat.last_message_timestamp = welcome_message.created_at
            chat.save()

            # Send an email notification
            subject = 'New chat created'
            message = f'A new chat has been created.\n\nUser details:\nEmail: {user.email}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}'
            from_email = 'misfotoscmbp@gmail.com'
            recipient_list = [admin_email]
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def message_list_create(request):
    """
    View to list messages or create a new message.

    GET:
        List all messages.
    POST:
        Create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save()            

            # Update the chat's unread_count fields if necessary
            if not message.user.is_admin:
                # Get the chat associated with the message
                chat = message.chat
                chat.unread = False
                chat.unread_count += 1
                chat.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def message_list_by_chat_id(request, chat_id, user_id):
    """
    View to list messages by chat ID.

    GET:
        List all messages for a specific chat.
    """
    try:
        messages = Message.objects.filter(chat_id=chat_id)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Get the chat associated with the chat_id
    try:
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
    except Chat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Update the chat's unread_count fields if necessary
    if user.is_admin:
        chat.unread = True
        chat.unread_count = 0
        chat.save()

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def chat_delete(request, chat_id):
    """
    View to delete a chat by its ID.

    DELETE:
        Delete a chat by its ID.
    """
    try:
        chat = get_object_or_404(Chat, pk=chat_id)
        chat.delete()
        return JsonResponse({'message': 'Chat deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
