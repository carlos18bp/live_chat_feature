/**
 * Utility functions for chat components.
 * @module chatUtils
 */

/**
 * Updates the rooms based on chats and admin data.
 * @param {Array} chats - The list of chats.
 * @param {Object} admin - The admin user data.
 * @param {string} avatarIcon - The path to the avatar icon.
 * @returns {Array} The updated list of rooms.
 */
export const updateRooms = (chats, admin, avatarIcon = '') => {
  if (!chats || chats.length === 0) {
    console.error('No chat available to update rooms');
    return [];
  }

  // Sort chats by lastMessageTimestamp
  const sortedChats = chats.map(chat => ({
    ...chat,
    lastMessageTimestamp: chat.messages.length > 0
      ? new Date(chat.messages[chat.messages.length - 1].created_at).getTime()
      : 0
  })).sort((a, b) => b.lastMessageTimestamp - a.lastMessageTimestamp);

  return sortedChats.map(chat => ({
    roomId: chat.id,
    roomName: `${chat.user.first_name} ${chat.user.last_name}`,
    avatar: avatarIcon,
    unreadCount: chat.unread_count,
    lastMessage: {
      content: chat.user.email,
    },
    users: [
      { _id: chat.user.email, username: `${chat.user.first_name} ${chat.user.last_name}` },
      { _id: admin.email, username: 'Admin Web Side' }
    ],
    lastMessageTimestamp: chat.lastMessageTimestamp
  }));
};

/**
 * Updates the messages based on new messages.
 * @param {Array} messages - The list of new messages.
 * @returns {Array} The updated list of messages.
 */
export const updateMessages = (messages) => {
  return messages.map(message => ({
    _id: message.id,
    content: message.text,
    senderId: message.user.email,
    timestamp: formatLocalTime(message.created_at),
    date: new Date(message.created_at).toLocaleDateString()
  }));
};

/**
 * Handles fetching messages for a specific room.
 * @param {Object} store - The chat store.
 * @param {Object} roomIdRef - The reference to the current room ID.
 * @param {Event} event - The fetch messages event.
 */
export const handleFetchMessages = async (store, roomIdRef, event) => {
  roomIdRef.value = event.detail[0].room.roomId;
  await store.fetchMessages(roomIdRef.value);
};

/**
 * Handles sending a message.
 * @param {Object} store - The chat store.
 * @param {string} userId - The ID of the current user.
 * @param {Event} event - The send message event.
 */
export const handleSendMessage = async (event, store, userId) => {
  const message = event.detail[0];
  const newMessage = {
    chat_id: message.roomId,
    user_email: userId,
    text: message.content,
    created_at: new Date().toISOString(),
  };
  try {
    await store.sendMessage(newMessage);
  } catch (error) {
    console.error('Failed to send message:', error);
  }
};

/**
 * Formats an ISO date string to local time (HH:mm).
 * @param {string} isoString - The ISO date string to format.
 * @returns {string} The formatted time string.
 */
export const formatLocalTime = (isoString) => {
  const date = new Date(isoString);
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  return `${hours}:${minutes}`;
};
  