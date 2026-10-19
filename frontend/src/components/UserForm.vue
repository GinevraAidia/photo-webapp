<template>
  <div class=" px-8 pt-6 pb-8 mb-4 items-center">

    <div v-if="loading">Caricamento in corso...</div>

   <form v-else @submit.prevent="updateProfile" class="flex flex-col items-center text-center px-4 pt-4 pb-4 mb-4 w-full">
  
      <div class="form-group flex flex-col items-center">
        <label for="username" class="mb-1 block font-medium">Username:</label>
        <input id="username" v-model="form.username" type="text" required class="border rounded px-1 py-1 text-center" />
        <small v-if="errors.username" class="error block text-red-500">{{ errors.username[0] }}</small>
      </div>

      <div class="form-group flex flex-col items-center">
        <label for="email" class="mb-1 block font-medium">Email:</label>
        <input id="email" v-model="form.email" type="email" required class="border rounded px-1 py-1 text-center" />
        <small v-if="errors.email" class="error block text-red-500 ">{{ errors.email[0] }}</small>
      </div>

      <button 
        type="submit" 
        :disabled="saving" 
        class="block mx-auto my-6 rounded-sm border border-[#8594E4] bg-white px-5 py-2 text-sm text-[#4C5DB2] shadow-sm transition-all duration-200
              hover:bg-[#8594E4] hover:text-white hover:shadow-md
              disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none">
        {{ saving ? 'Salvataggio...' : 'Salva Modifiche' }}
      </button>

      <p v-if="successMessage" class="success text-green-600 mt-2">{{ successMessage }}</p>
      <p v-if="generalError" class="error text-red-600 mt-2">{{ generalError }}</p>
      
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import type { UserFormData } from "@/types/post"
import { userService } from '@/services/userService'

interface UserProfile {
  id: number
  username: string
  email: string
}

const form = ref({
  username: '',
  email: ''
})

const loading = ref(true)
const saving = ref(false)
const successMessage = ref('')
const generalError = ref('')
const errors = ref<Record<string, string[]>>({})

// 1. Recupera i dati utente
const fetchProfile = async () => {
  loading.value = true
  generalError.value = ''
  try {
    const response = await api.get<UserProfile>('events/users/me/')
    form.value.username = response.data.username
    form.value.email = response.data.email
  } catch (err: any) {
    generalError.value = 'Errore nel caricamento del profilo.'
  } finally {
    loading.value = false
  }
}

// 2. Aggiorna i dati utente
const updateProfile = async () => {
  saving.value = true
  successMessage.value = ''
  generalError.value = ''
  errors.value = {}

  try {
   const payload: UserFormData = {
      username: form.value.username,
      email: form.value.email,
    }
    const response =await userService.update( payload)
    form.value.username = response.username
    form.value.email = response.email
    successMessage.value = 'Profilo aggiornato con successo!'
  } catch (err: any) {
    if (err.response && err.response.data) {
      errors.value = err.response.data
    } else {
      generalError.value = 'Impossibile aggiornare i dati.'
    }
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>
