from django.urls import path
from live_chat_app.views import chat

urlpatterns = [
    path('admin_web_side/', chat.admin_get_or_create, name='admin_get_or_create'),
    path('user/', chat.user_get_or_create, name='user_get_or_create'),
    path('messages/', chat.message_list_create, name='message_list_create'),
    path('messages/<int:chat_id>/user/<int:user_id>', chat.message_list_by_chat_id, name='message_list_by_chat_id'),
    path('chats/', chat.chat_list_create, name='chat_list_create'),
    path('chat_delete/<int:chat_id>/', chat.chat_delete, name='chat_delete'),
]
