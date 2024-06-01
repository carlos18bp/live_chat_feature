<template>
  <vue-advanced-chat
    height="500px"
    :current-user-id="userId"
    :rooms="rooms"
    :rooms-loaded="roomsLoaded"
    :single-room="true"
    :loading-rooms="true"
    :room-message="messageByDefault"
    :show-add-room="false"
    :messages="messages"
    :messages-loaded="messagesLoaded"
    :show-reaction-emojis="false"
    :show-audio="false"
    :show-files="false"    
    :theme="'light'"
    @fetch-messages="handleFetchMessages"
    @send-message="sendMessage"
  />
</template>

<script setup>
  import { ref, onMounted, watch } from 'vue';
  import { register } from 'vue-advanced-chat';
  import avatarIcon from '@/assets/avatar-icon.png';
  import { useChatStore } from '@/store/chat';
  import { useSocketStore } from '@/store/socket';
  import { updateRooms, updateMessages, handleSendMessage } from '@/utils/chatUtils';

  // Register the vue-advanced-chat component
  register();

  const store = useChatStore();
  const socketStore = useSocketStore();
  const userStarted = ref(false);
  const userId = ref(null);
  const roomsLoaded = ref(false);
  const messagesLoaded = ref(false);
  const messageByDefault = ref('');

  const rooms = ref([]);
  const messages = ref([]);
  const currentRoomId = ref(null);

  // Lifecycle hook to initialize the component
  onMounted(async () => {
    try {
      await store.fetchAdmin();

      // Set up WebSocket message listener
      socketStore.socket.onmessage = async (event) => {
        const data = JSON.parse(event.data);
        if (data.action === 'update_chat' && currentRoomId.value) {
          await store.createAndAssignChat();
          await store.fetchMessages(currentRoomId.value, store.user.id);
        }
      };

      // Initialize user if found in local storage
      const user = localStorage.getItem('user');
      if (user) userStart(JSON.parse(user));

      messageByDefault.value = "I'd like more information";
    } catch (error) {
      console.error('Failed to initialize chats or messages:', error);
    }
  });

  // Watcher for store user changes
  watch(() => store.user, async (user) => {  
    if (!userStarted.value) userStart(user);
    userStarted.value = true;
  });

  // Watcher for store chats changes
  watch(() => store.chats, (newChats) => {
    rooms.value = updateRooms(newChats, store.admin, avatarIcon);
    roomsLoaded.value = true;
  });

  // Watcher for store messages changes
  watch(() => store.messages, (newMessages) => {
    messages.value = updateMessages(newMessages);
    messagesLoaded.value = true;
  });

  /**
   * Starts the user session and fetches or creates a user.
   * @param {Object} user - The user data.
   */
  const userStart = async (user) => {
    await store.fetchOrCreateUser(user);
    await store.createAndAssignChat();
    userId.value = store.user.email;
    socketStore.sendMessage('update_chat');
  };

  /**
   * Handles fetching messages for a specific room.
   * @param {Event} event - The fetch messages event.
   */
  const handleFetchMessages = (event) => {
    currentRoomId.value = event.detail[0].room.roomId;
    store.fetchMessages(currentRoomId.value, store.user.id);
  };

  /**
   * Handles sending a message.
   * @param {Event} event - The send message event.
   */
  const sendMessage = async (event) => {
    handleSendMessage(event, store, userId.value)
  };
</script>

<style scoped>
  .chat-container {
    display: flex;
    height: 100vh;
  }

  .chat-window {
    flex-grow: 1;
    padding: 20px;
  }
</style>
