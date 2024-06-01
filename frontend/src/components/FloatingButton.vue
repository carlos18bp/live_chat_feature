<template>
  <div>
    <div class="floating-button fixed bottom-5 right-5 bg-blue-500 text-white rounded-full p-2 shadow-lg cursor-pointer hover:bg-blue-700" @click="toggleInitLiveChat">
      <img v-if="showForm || showChat" src="@/assets/chat-open-icon.png" alt="Chat Icon" class="size-10" />
      <img v-else src="@/assets/chat-icon.png" alt="Chat Icon" class="size-10" />
    </div>
    <div v-if="showForm" class="floating-form fixed bottom-20 right-5 bg-white border border-gray-300 rounded-lg shadow-lg p-4 z-50">
      <ChatInitForm @chat-started="handleChatStarted" />
    </div>
    <div v-show="showChat" class="chat-window fixed bottom-20 right-5 bg-white border border-gray-300 rounded-lg shadow-lg z-50">
      <ChatComponent />
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import ChatInitForm from '@/components/ChatInitForm.vue'
  import ChatComponent from '@/components/ChatComponent.vue'

  // Reactive variables to control form and chat visibility
  const showForm = ref(false);
  const showChat = ref(false);

  //onMounted(() => localStorage.removeItem('user'));

  /**
   * Toggle the visibility of the form.
   * If a user is already stored in localStorage, toggles chat visibility instead.
   */
  const toggleInitLiveChat = () => {
    if (localStorage.getItem('user') === null) {
      showForm.value = !showForm.value;
    } else {
      showChat.value = !showChat.value;
    }
  }

  /**
   * Handle chat started event.
   * Hides the form and shows the chat window.
   */
  const handleChatStarted = () => {
    showForm.value = false;
    showChat.value = true;
  }
</script>

<style scoped>
  .floating-button {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .floating-form {
    width: 300px;
  }

  .chat-window {
    width: 400px;
    height: 500px;
  }
</style>
