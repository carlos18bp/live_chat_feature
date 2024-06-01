import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/admin_live_chat',
    name: 'admin_live_chat',
    component: () => import('@/views/Admin.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
export { routes };
