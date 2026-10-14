<template>

<nav class="bg-neutral-primary fixed w-full z-20 top-0 start-0 border-b border-default">
  <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto px-4">
    <a href="https://aidia.it/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <span class="self-center text-xl text-heading font-semibold whitespace-nowrap">Aidia</span>
    </a>
    <div class="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
        <button v-if="authStore.hasSession" type="button" @click="$router.push('/UserProfile')" class="inline-flex flex-col items-center justify-center px-5 hover:bg-neutral-secondary-medium group">
          <svg class="w-6 h-6 mb-1 text-body group-hover:text-fg-brand" aria-hidden="true" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0 0a8.949 8.949 0 0 0 4.951-1.488A3.987 3.987 0 0 0 13 16h-2a3.987 3.987 0 0 0-3.951 3.512A8.948 8.948 0 0 0 12 21Zm3-11a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/></svg>
          <span class="text-sm text-body group-hover:text-fg-brand">Profile</span>
        </button>
        <button type="button" class="rounded-xl border border-[#8594E4]
         bg-white px-5 py-2
         font-small text-[#4C5DB2]
         shadow-sm
         hover:bg-[#8594E4] hover:text-white
         hover:shadow-md" @click="handleLogin">{{ authStore.hasSession ? 'Logout' : 'Accedi' }}</button>
         
    </div>
    <div class="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
      <ul class="flex flex-col p-4 md:p-0 mt-4 font-medium border border-default rounded-base bg-neutral-secondary-soft md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-neutral-primary">
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

const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  if (authStore.hasSession) {
    await authStore.logout()
    await router.push('/login')
  } else {
    await router.push('/login')
  }
}
</script>