<template>
    <div class="login-container">
        <form @submit.prevent="handleLogin">
            <input v-model="username" type="text" placeholder="Username" />
            <input v-model="password" type="password" placeholder="Password" />
        
            <button type="submit" :disabled="loading">
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

