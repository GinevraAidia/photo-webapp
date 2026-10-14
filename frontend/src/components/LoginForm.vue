<template>
    <div class="login-container">
        <form @submit.prevent="handleLogin" class="space-y-8 m-4">
            <input v-model="username" type="text" placeholder="Username" class="rounded-xl border border-[#8594E4] bg-white px-5 py-2 font-medium text-[#4C5DB2] shadow-sm hover:bg-[#8594E4] hover:text-white hover:shadow-md transition-all duration-300"/>
            <input v-model="password" type="password" placeholder="Password" class="rounded-xl border border-[#8594E4] bg-white px-5 py-2 font-medium text-[#4C5DB2] shadow-sm hover:bg-[#8594E4] hover:text-white hover:shadow-md transition-all duration-300" />
        
            <button type="submit" :disabled="loading" class="rounded-xl border border-[#8594E4] bg-white px-5 py-2 font-medium text-[#4C5DB2] shadow-sm hover:bg-[#8594E4] hover:text-white hover:shadow-md transition-all duration-300">
            {{ loading ? 'Accesso in corso...' : 'Login' }}
            </button>
            <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
        </form>
    </div>
    
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''
  
  try {
    // Chiama l'action di Pinia
    await authStore.login({
      username: username.value,
      password: password.value,
    })
    
   console.log('Login riuscito, reindirizzamento...')
   router.push('/events')
  } catch (err: any) {
    errorMessage.value = 'Credenziali non valide o server non raggiungibile.'
    console.error('Errore durante il login:', err)
  } finally {
    loading.value = false
  }
}
</script>

