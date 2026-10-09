<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Event, EventFormData } from '@/types/post'

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
  submit: [data: EventFormData]
}>()

const editTitle = ref('')
const editDescription = ref('')
const editVisibility = ref<'public' | 'private'>('public')
const editUsers = ref<number[]>([])
const usernameChosen = ref<number | null>(null)

watch(
  () => props.event,
  (event) => {
    editTitle.value = event?.title ?? ''
    editDescription.value = event?.description ?? ''
    editVisibility.value = event?.visibility ?? 'public'
    editUsers.value = [...(event?.users ?? [])]
    usernameChosen.value = null
  },
  { immediate: true }
)

function addUserToList() {
  if (
    usernameChosen.value !== null &&
    !editUsers.value.includes(usernameChosen.value)
  ) {
    editUsers.value.push(usernameChosen.value)
  }

  usernameChosen.value = null
}

function onSubmit() {
  emit('submit', {
    title: editTitle.value,
    description: editDescription.value,
    visibility: editVisibility.value,
    users: editUsers.value
  })
}
</script>

<template>
  <div class="modal-overlay">
    <div class="event-form" @click.stop>
      <button class="close-btn" @click="emit('cancel')">×</button>

      <h2>{{ event ? 'Modifica evento' : 'Nuovo evento' }}</h2>

        <form @submit.prevent="onSubmit">
        <input v-model="editTitle" type="text" placeholder="Titolo" required />

        <input
          v-model="editDescription"
          type="text"
          placeholder="Descrizione"
        />

        <select v-model="editVisibility">
          <option value="public">Pubblico</option>
          <option value="private">Privato</option>
        </select>

        <span>Seleziona gli utenti</span>

        <select v-model="usernameChosen" @change="addUserToList">
          <option :value="null" disabled>Seleziona un utente</option>
          <option
            v-for="user in users"
            :key="user.id"
            :value="user.id"
          >
            {{ user.username }}
          </option>
        </select>

        <div v-if="editUsers.length > 0">
          <p>Utenti selezionati:</p>
          <ul>
            <li v-for="userId in editUsers" :key="userId">
              {{ users.find(user => user.id === userId)?.username }}
              <button
                type="button"
                @click="editUsers = editUsers.filter(id => id !== userId)"
              >
                ×
              </button>
            </li>
          </ul>
        </div>
        <button type="submit">
        {{ event ? 'Salva modifiche' : 'Crea evento' }}
        </button>
      </form>
    </div>
  </div>
</template>