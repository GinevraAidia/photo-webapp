import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import { useAuthStore } from '@/stores/auth'
import EventsView from '@/views/EventsView.vue'
import PostsView from '@/views/PostsView.vue'
import HomeView from '@/views/HomeView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('../views/HomeView.vue')
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
    }
  ],
})
router.beforeEach((to) => {
  const authStore = useAuthStore()
  if( to.meta.requiresAuth && !authStore.isAuthenticated) {
    return '/login' //se non è autenticato lo rimando alla pagina di login
  }
})
export default router
