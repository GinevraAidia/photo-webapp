<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

import PostCard from '@/components/PostCard.vue'
import PostForm from '@/components/PostForm.vue'
import { postService } from '@/services/postService'
import type { Post } from '@/types/post'
import api from '@/services/api'

const route = useRoute()

const posts = ref<Post[]>([])
const isCreating = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const event = ref<EventData | null>(null)

interface EventData {
  id: number
  title: string
}
const eventId = computed(() => {
  const value = Number(route.query.event)

  return Number.isInteger(value) && value > 0
    ? value
    : null
})

async function loadEvent() {
  if (eventId.value === null) {
    event.value = null
    return
  }

  try {
    const response = await api.get<EventData>(
      `/events/event/${eventId.value}/`
    )

    event.value = response.data
  } catch (error) {
    console.error('Errore caricamento evento:', error)
    event.value = null
  }
}
const empty = computed(
  () => !loading.value && posts.value.length === 0
)

async function loadPosts() {
  if (eventId.value === null) {
    posts.value = []
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    posts.value = await postService.getByEvent(eventId.value)
  } catch {
    errorMessage.value = 'Impossibile caricare i post.'
  } finally {
    loading.value = false
  }
}

function removePost(id: number) {
  posts.value = posts.value.filter(post => post.id !== id)
}

function updatePost(updated: Post) {
  const index = posts.value.findIndex(
    post => post.id === updated.id
  )

  if (index !== -1) {
    posts.value[index] = updated
  }
}

watch(eventId, () => {
  loadPosts()
  loadEvent()
}, { immediate: true })
</script>

<template>
  <section>
    <div class="grid grid-cols-3 items-center mb-4">
       <button @click="isCreating = true" class="justify-self-start px-4 py-2 bg-blue-600 text-white rounded-lg">
            Nuovo post
        </button> 
    <h1 class="text-center text-4xl font-bold tracking-tight text-heading md:text-5xl lg:text-6xl">{{ event?.title ?? 'Caricamento evento...' }}</h1>
    </div>
    <p v-if="loading">Caricamento...</p>
    <p v-if="errorMessage" role="alert">
      {{ errorMessage }}
    </p>
    <p v-if="empty">Non ci sono post.</p>

    <PostCard v-for="post in posts" :key="post.id" :post="post" @deleted="removePost" @updated="updatePost"/>

    <div v-if="isCreating" class="modal-overlay">
      <PostForm :event-id="eventId" :post="null" @saved="post => posts.push(post)" @cancel="isCreating = false"/>
    </div>
  </section>
</template>