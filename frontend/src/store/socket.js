import { defineStore } from 'pinia';
import { ref } from 'vue';

/**
 * Pinia store for managing WebSocket connections and actions.
 */
export const useSocketStore = defineStore('socket', () => {
  const socket = new WebSocket('ws://127.0.0.1:8000/ws/chat/'); // Connect to the global WebSocket group

  const isConnected = ref(false);
  const message = ref('');

  /**
   * Handles WebSocket connection open event.
   */
  socket.onopen = () => {
    isConnected.value = true;
    console.log('Connected to WebSocket server');
  };

  /**
   * Handles WebSocket connection close event.
   */
  socket.onclose = () => {
    isConnected.value = false;
    console.log('Disconnected from WebSocket server');
  };

  /**
   * Handles incoming WebSocket messages.
   * @param {MessageEvent} event - The incoming message event.
   */
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    message.value = data;
    handleAction(data);
  };

  /**
   * Sends a message through the WebSocket.
   * @param {string} action - The action to send.
   */
  const sendMessage = (action = 'new_chat') => {
    if (socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ action }));
    }
  };

  /**
   * Handles different WebSocket actions.
   * @param {Object} data - The data received from the WebSocket.
   */
  const handleAction = (data) => {
    switch (data.action) {
      case 'update_chat':
        // Handle the update_chat action
        console.log('Update chat action received');
        break;
      default:
        console.log('Unknown action received', data.action);
    }
  };

  return { socket, isConnected, message, sendMessage };
});
