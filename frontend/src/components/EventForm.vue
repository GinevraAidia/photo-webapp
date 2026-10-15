<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { Event, EventFormData } from '@/types/post'
import { eventService } from '@/services/eventService'

interface User {
  id: number
  username: string
  email: string
}

const props = defineProps<{
  event: Event | null
  users: User[]
}>()

const emit = defineEmits<{
  cancel: []
  saved: [] // Segnala al genitore che il DB è stato aggiornato con successo
}>()

const editTitle = ref('')
const editDescription = ref('')
const editVisibility = ref<'public' | 'private'>('public')
const editUsers = ref<number[]>([])
const usernameChosen = ref<number | null>(null)

// Gestione stato di caricamento durante la chiamata di rete
const isSaving = ref(false)

const usersMap = computed(() => {
  return new Map(props.users.map(user => [user.id, user.username]))
})

watch(
  () => props.event, //funzione getter per il valore da osservare (dinamica)
  (event) => { //funz eseguita quando il valore cambia
    editTitle.value = event?.title ?? ''
    editDescription.value = event?.description ?? ''
    editVisibility.value = event?.visibility ?? 'public'
    editUsers.value = event?.users ? [...event.users] : []
    usernameChosen.value = null
  },
  { immediate: true }
)

function addUserToList() {
  if (usernameChosen.value !== null && !editUsers.value.includes(usernameChosen.value)) {
    editUsers.value.push(usernameChosen.value)
  }
  usernameChosen.value = null
}

function removeUserFromList(userId: number) {
  editUsers.value = editUsers.value.filter(id => id !== userId)
}

async function onSubmit() {
  isSaving.value = true

  const payload: EventFormData = {
    title: editTitle.value,
    description: editDescription.value,
    visibility: editVisibility.value,
    users: editUsers.value
  }

  try {
    if (props.event?.id) {
      await eventService.update(props.event.id, payload)
    } else {
      await eventService.create(payload)
    }

    // Notifica il genitore per aggiornare la lista e chiude il modale
    emit('saved')
    emit('cancel')

  } catch (error) {
    console.error('Errore durante la chiamata API:', error)
    alert('Impossibile salvare i dati a database. Controlla che il backend su localhost:8000 sia attivo.')
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div class="modal-overlay" @click="emit('cancel')">
    <div class="event-form" @click.stop>
      <button type="button" class="close-btn" :disabled="isSaving" @click="emit('cancel')">×</button>

      <h2>{{ event ? 'Modifica evento' : 'Nuovo evento' }}</h2>

      <form @submit.prevent="onSubmit">
        <input v-model="editTitle" type="text" placeholder="Titolo" required :disabled="isSaving" />

        <input v-model="editDescription" type="text" placeholder="Descrizione" :disabled="isSaving" />

        <select v-model="editVisibility" :disabled="isSaving">
          <option value="public">Pubblico</option>
          <option value="private">Privato</option>
        </select>

        <label for="user-select">Seleziona gli utenti</label>
        <select id="user-select" v-model="usernameChosen" :disabled="isSaving" @change="addUserToList">
          <option :value="null" disabled selected>Seleziona un utente</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>

        <div v-if="editUsers.length > 0" class="selected-users">
          <p>Utenti selezionati:</p>
          <ul>
            <li v-for="userId in editUsers" :key="userId">
              {{ usersMap.get(userId) || 'Utente sconosciuto' }}
              <button 
                type="button" 
                :disabled="isSaving" 
                @click="removeUserFromList(userId)"
              >
                ×
              </button>
            </li>
          </ul>
        </div>

        <button type="submit" :disabled="isSaving">
          {{ isSaving ? 'Salvataggio...' : (event ? 'Salva modifiche' : 'Crea evento') }}
        </button>
      </form>
    </div>
  </div>
</template>
