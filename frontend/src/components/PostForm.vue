<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Post, PostFormData } from '@/types/post'
import { postService } from '@/services/postService'

const props = withDefaults(defineProps<{
  eventId?: number | null
  post?: Post | null
}>(), {
  eventId: null,
  post: null
})

const emit = defineEmits<{
  cancel: []
  saved: [post: Post] // Segnala al genitore che il DB è stato aggiornato con successo
}>()

const description = ref('')
const image = ref<File | null>(null)

// Gestione stato di caricamento durante la chiamata di rete
const isSaving = ref(false)

watch(
  () => props.post,
  (post) => {
    description.value = post?.description ?? ''
    image.value = null
  },
  { immediate: true }
)

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  image.value = input.files?.[0] ?? null
}

async function onSubmit() {
  if (!props.post?.id && props.eventId === null) return

  isSaving.value = true

  const payload: PostFormData = {
    description: description.value,
    image: image.value
  }

  try {
    let saved: Post

    if (props.post?.id) {
      saved = await postService.update(props.post.id, payload)
    } else {
      saved = await postService.create(props.eventId as number, payload)
    }

    // Notifica il genitore per aggiornare la lista e chiude il modale
    emit('saved', saved)
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
    <div class="event-form" @click.stop>
        <form @submit.prevent="onSubmit">
            <input
            v-model="description"
            type="text"
            placeholder="Descrizione"
            :disabled="isSaving"
            />

            <input
            type="file"
            accept="image/*"
            :disabled="isSaving"
            @change="onFileChange"
            />

            <button type="submit" :disabled="isSaving">
            {{ isSaving ? 'Salvataggio...' : (post ? 'Salva modifiche' : 'Crea post') }}
            </button>

            <button type="button" :disabled="isSaving" @click="emit('cancel')">
            Annulla
            </button>
        </form>
    </div>
</template>
