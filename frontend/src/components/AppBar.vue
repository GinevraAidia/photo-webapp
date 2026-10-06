<template>

<nav class="bg-neutral-primary fixed w-full z-20 top-0 start-0 border-b border-default">
  <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
    <a href="https://aidia.it/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <span class="self-center text-xl text-heading font-semibold whitespace-nowrap">Aidia</span>
    </a>
    <div class="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
        <button type="button" class="text-white bg-brand hover:bg-brand-strong box-border border border-transparent focus:ring-4 focus:ring-brand-medium shadow-xs font-medium leading-5 rounded-base text-sm px-3 py-2 focus:outline-none" @click="handleLogin">{{ authStore.isAuthenticated ? 'Logout' : 'Accedi' }}</button>
    </div>
    <div class="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
      <ul class="flex flex-col p-4 md:p-0 mt-4 font-medium border border-default rounded-base bg-neutral-secondary-soft md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-neutral-primary">
        <li>
          <router-link class="block py-2 px-3 text-heading bg-brand rounded-sm md:bg-transparent md:text-fg-brand md:p-0" to="/">Home</router-link>
        </li>
        <li>
          <router-link class="block py-2 px-3 text-heading rounded hover:bg-neutral-tertiary md:hover:bg-transparent md:border-0 md:hover:text-fg-brand md:p-0 md:dark:hover:bg-transparent" to="/events">Events</router-link>
        </li>
      </ul>
    </div>
  </div>
</nav>

</template>
<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginForm from './LoginForm.vue' // Assicurati che il percorso sia corretto
import { ref } from 'vue'
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = () => {
  // 1. Esegui la pulizia dello store e del localStorage
  if(authStore.isAuthenticated){
    authStore.logout()

  }
  // 2. Reindirizza subito l'utente al login
  router.push('/login')
}
</script>
