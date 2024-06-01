<template>
  <router-view />
</template>

<script setup>
  import { provide } from 'vue';
  import { useChatStore } from '@/store/chat';

  const store = useChatStore();
  provide('chatStore', store);
</script>

<style>
/* Add your styles here */
</style>
