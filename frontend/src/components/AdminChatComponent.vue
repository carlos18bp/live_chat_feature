<template>
  <div class="p-2">
    <vue-advanced-chat    
      height="calc(100vh - 20px)"
      :current-user-id="adminId"
      :rooms="rooms"
      :rooms-loaded="roomsLoaded"
      :room-info-enabled="true"
      :room-actions="JSON.stringify(roomActions)"
      :loading-rooms="false"
      :show-add-room="false"
      :messages="messages"
      :messages-loaded="messagesLoaded"
      :message-actions="JSON.stringify(messageActions)"
      :templates-text="JSON.stringify(templatesText)"
      :show-reaction-emojis="false"
      :show-audio="false"
      :show-files="false"     
      :theme="'dark'"      
      @room-action-handler="menuActionHandler" 
      @fetch-messages="handleFetchMessages"
      @send-message="sendMessage"
    >
      <div slot="room-header" class="flex space-x-2">
        <img class="size-10" src="@/assets/avatar-icon.png" alt="User Avatar">
        <div>
          <div class="font-bold">{{ userFullNameFocus }}</div>
          <div class="text-xs">{{ userEmailFocus }}</div>
        </div>
      </div>
    </vue-advanced-chat>  
  </div>
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
  const adminId = ref('admin@example.com');
  const userFullNameFocus = ref('');
  const userEmailFocus = ref('');
  const roomsLoaded = ref(false);
  const messagesLoaded = ref(false);
  const rooms = ref([]);
  const messages = ref([]);
  const currentRoomId = ref(null);

  // Templates for messages
  const templatesText = [
    { tag: 'help', text: 'This is the help' },
    { tag: 'action', text: 'This is the action' }
  ];

  // Actions for messages
  const messageActions = [
    { name: 'replyMessage', title: 'Reply' },
    { name: 'selectMessages', title: 'Select' }
  ];

  // Actions for rooms
  const roomActions = [
    { name: 'deleteChat', title: 'Delete chat' }
  ];

  // Lifecycle hook to initialize the component
  onMounted(async () => {
    try {
      await store.fetchAdmin();
      adminId.value = store.admin.email;
      await store.fetchChats();
    } catch (error) {
      console.error('Failed to initialize chats or messages:', error);
    }

    // Set up WebSocket message listener
    socketStore.socket.onmessage = async (event) => {
      const data = JSON.parse(event.data);
      if (data.action === 'update_chat' && currentRoomId.value) {      
        await store.fetchMessages(currentRoomId.value, store.admin.id);
        await store.fetchChats();
      }
    };
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
   * Handles fetching messages for a specific room.
   * @param {Event} event - The fetch messages event.
   */
  const handleFetchMessages = async (event) => {
    userFullNameFocus.value = event.detail[0].room.roomName;
    userEmailFocus.value = event.detail[0].room.users[0]._id;
    
    currentRoomId.value = event.detail[0].room.roomId;
    await socketStore.sendMessage('update_chat');
  };

  /**
   * Handles sending a message.
   * @param {Event} event - The send message event.
   */
  const sendMessage = async (event) => {
    handleSendMessage(event, store, adminId.value)
  };
</script>

<style scoped>
  .admin-chat-container {
    display: flex;
    height: 100vh;
  }

  .chat-window {
    flex-grow: 1;
    padding: 20px;
  }
</style>
