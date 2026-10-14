<script setup lang="ts">
import { ref, computed } from 'vue'
import type { EventFormData } from '@/types/post'

interface User {
  id: number
  username: string
  email: string
}

const props = withDefaults(defineProps<{
  initialTitle?: string
  initialDescription?: string
  initialVisibility?: 'public' | 'private'
  initialUsers?: number[]
  submitLabel?: string
  loading?: boolean
  users?: User[]
}>(), {
  initialTitle: '',
  initialDescription: '',
  initialVisibility: 'public',
  initialUsers: () => [],
  submitLabel: 'Salva',
  loading: false,
  users: () => []
})

const emit = defineEmits<{
  submit: [data: EventFormData]
  cancel: []
}>()

const title = ref(props.initialTitle)
const description = ref(props.initialDescription)
const visibility = ref<'public' | 'private'>(props.initialVisibility)
const selectedUsers = ref<number[]>([...props.initialUsers])
const chosenUser = ref<number | null>(null)

const usersMap = computed(() => {
  return new Map(props.users.map(user => [user.id, user.username]))
})

function addUserToList() {
  if (chosenUser.value !== null && !selectedUsers.value.includes(chosenUser.value)) {
    selectedUsers.value.push(chosenUser.value)
  }
  chosenUser.value = null
}

function removeUserFromList(userId: number) {
  selectedUsers.value = selectedUsers.value.filter(id => id !== userId)
}

function onSubmit() {
  emit('submit', {
    title: title.value,
    description: description.value,
    visibility: visibility.value,
    users: selectedUsers.value
  })
}
</script>

<template>
    <div class="event-form" @click.stop>
        <form @submit.prevent="onSubmit">
            <input
            v-model="title"
            type="text"
            placeholder="Titolo"
            required
            :disabled="loading"
            />

            <input
            v-model="description"
            type="text"
            placeholder="Descrizione"
            :disabled="loading"
            />

            <select v-model="visibility" :disabled="loading">
                <option value="public">Pubblico</option>
                <option value="private">Privato</option>
            </select>

            <label for="user-select">Seleziona gli utenti</label>
            <select
            id="user-select"
            v-model="chosenUser"
            :disabled="loading"
            @change="addUserToList"
            >
                <option :value="null" disabled selected>Seleziona un utente</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                    {{ user.username }}
                </option>
            </select>

            <div v-if="selectedUsers.length > 0" class="selected-users">
                <p>Utenti selezionati:</p>
                <ul>
                    <li v-for="userId in selectedUsers" :key="userId">
                        {{ usersMap.get(userId) || 'Utente sconosciuto' }}
                        <button
                        type="button"
                        :disabled="loading"
                        @click="removeUserFromList(userId)"
                        >
                            ×
                        </button>
                    </li>
                </ul>
            </div>

            <button type="submit" :disabled="loading">
                {{ loading ? 'Salvataggio...' : submitLabel }}
            </button>

            <button type="button" @click="emit('cancel')">
                Annulla
            </button>
        </form>
    </div>
</template>
