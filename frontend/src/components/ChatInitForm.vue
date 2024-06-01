<template>
  <div class="chat-init-form p-4 bg-white rounded-lg shadow-md">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
        <input type="email" v-model="userForm.email" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm" />
      </div>
      <div>
        <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
        <input type="text" v-model="userForm.first_name" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm" />
      </div>
      <div>
        <label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
        <input type="text" v-model="userForm.last_name" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm" />
      </div>
      <button type="submit" class="w-full bg-blue-500 text-white py-2 px-4 rounded-md shadow-sm hover:bg-blue-700">Start Chat</button>
    </form>
  </div>
</template>

<script setup>
  import { reactive } from 'vue'
  import { useChatStore } from '@/store/chat'

  // Emit event
  const emit = defineEmits(['chat-started'])
  const store = useChatStore()

  // Reactive form data
  const userForm = reactive({
    email: '',
    first_name: '',
    last_name: ''
  });

  /**
   * Handle form submission.
   * Fetches or creates a user based on the form data,
   * saves the user data to localStorage, and emits a 'chat-started' event.
   */
  const handleSubmit = async () => {
    try {
      await store.fetchOrCreateUser(userForm);
      
      // Save the user in localStorage
      localStorage.setItem('user', JSON.stringify(store.user));
      
      emit('chat-started');
    } catch (error) {
      console.error('Failed to start chat:', error);
    }
  }
</script>

<style scoped>
  .chat-init-form {
    max-width: 400px;
    margin: 0 auto;
  }
</style>
