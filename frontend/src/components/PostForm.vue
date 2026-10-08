<script setup lang="ts">
import { ref } from 'vue'
import type { PostFormData } from '@/types/post'

const props = withDefaults(defineProps<{
  initialDescription?: string
  submitLabel?: string
  loading?: boolean
}>(), {
  initialDescription: '',
  submitLabel: 'Salva',
  loading: false
})

const emit = defineEmits<{
  submit: [data: PostFormData]
  cancel: []
}>()

const description = ref(props.initialDescription)
const image = ref<File | null>(null)

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  image.value = input.files?.[0] ?? null
}

function onSubmit() {
  emit('submit', {
    description: description.value,
    image: image.value
  })
}
</script>

<template>
    <div class="event-form" @click.stop>
        <form @submit.prevent="onSubmit">
            <input
            v-model="description"
            type="text"
            placeholder="Descrizione"
            />

            <input
            type="file"
            accept="image/*"
            @change="onFileChange"
            />

            <button type="submit" :disabled="loading">
            {{ loading ? 'Salvataggio...' : submitLabel }}
            </button>

            <button type="button" @click="emit('cancel')">
            Annulla
            </button>
        </form>
    </div>
  
</template>