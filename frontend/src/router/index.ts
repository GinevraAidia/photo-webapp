import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('../views/EventsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path:'/events',
      component: () => import('../views/EventsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path:'/posts',
      component: () => import('../views/PostsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path:'/UserProfile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    } 
  ],
})
router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth &&!authStore.hasSession) {
  return '/login'
  }
  if(to.path === '/login' && authStore.hasSession){
    return '/'
  }
  return true
})
export default router
