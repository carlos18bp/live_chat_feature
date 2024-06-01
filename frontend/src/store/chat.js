import { defineStore } from 'pinia';
import { useSocketStore } from './socket';
import { get_request, create_request, delete_request } from "./services/request_http";

/**
 * Pinia store for managing chat-related state and actions.
 */
export const useChatStore = defineStore('chat', {
  state: () => ({
    user: null,
    messages: [],
    chats: [],
    admin: null,
    currentRoomId: null,
  }),
  actions: {
    /**
     * Fetches admin data from the server.
     */
    async fetchAdmin() {
      try {
        const data = await create_request('admin_web_side/', {});
        this.admin = data;
      } catch (error) {
        console.error('Failed to fetch admin ID:', error);
      }
    },
    /**
     * Fetches or creates a user based on the provided user data.
     * @param {Object} user - The user data.
     */
    async fetchOrCreateUser(user) {
      try {
        const data = await create_request('user/', JSON.stringify(user));
        this.user = data;
      } catch (error) {
        console.error('Failed to create user:', error);
      }
    },
    /**
     * Creates and assigns a chat between the user and the admin.
     */
    async createAndAssignChat() {
      await this.fetchAdmin();
      if (!this.admin) {
        console.error('Admin is undefined');
        return;
      }
      if (!this.user) {
        console.error('User is undefined');
        return;
      }
      
      const chat = {
        user_email: this.user.email,
        admin_email: this.admin.email
      };
      const data = await create_request('chats/', JSON.stringify(chat));     
      this.chats = [data];      
    },
    /**
     * Fetches all chats from the server.
     */
    async fetchChats() {
      try {
        const data = await get_request('chats/');
        if (!Array.isArray(data)) {
          throw new Error('Invalid response data');
        }
        this.chats = data;
      } catch (error) {
        console.error('Failed to fetch chats:', error);
      }
    },
    /**
     * Deletes a chat with the specified ID.
     * @param {number} chatId - The ID of the chat to delete.
     */
    async deleteChat(chatId) {
      try {
        await delete_request(`chat_delete/${chatId}/`);
        this.fetchChats();
      } catch (error) {
        console.error('Failed to remove chat:', error);
      }
    },
    /**
     * Fetches messages for a specific chat.
     * @param {number} chatId - The ID of the chat to fetch messages for.
     */
    async fetchMessages(chatId, userId) {
      if (!chatId) {
        console.error('Chat ID is undefined');
        return;
      }
      chatId = parseInt(chatId, 10);
      if (isNaN(chatId)) {
        console.error('Chat ID is not a valid number');
        return;
      }

      this.currentRoomId = chatId;  // Save the current room ID
      try {
        const data = await get_request(`messages/${chatId}/user/${userId}`);
        this.messages = Array.isArray(data) ? data : [];
      } catch (error) {
        console.error('Failed to fetch messages:', error);
      }
    },
    /**
     * Sends a message.
     * @param {Object} message - The message data to send.
     * @returns {Object} The new message data from the server.
     */
    async sendMessage(message) {
      await create_request('messages/', JSON.stringify(message));

      // Send the message through the WebSocket
      const socketStore = useSocketStore();
      socketStore.sendMessage('update_chat');
    },
  },
});
