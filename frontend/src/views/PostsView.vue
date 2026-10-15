<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

import PostCard from '@/components/PostCard.vue'
import PostForm from '@/components/PostForm.vue'
import type { Post } from '@/types/post'
import api from '@/services/api'

interface EventData {
  id: number
  title: string
}

const route = useRoute()

const posts = ref<Post[]>([])
const isCreating = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const event = ref<EventData | null>(null)

const currentPage = ref(1)
const totalCount = ref(0)
const perPage = ref(2) 

const totalPages = computed(() => {
  return Math.ceil(totalCount.value / perPage.value) || 1
})

const eventId = computed(() => {
  const value = Number(route.query.event)
  return Number.isInteger(value) && value > 0 ? value : null
})

async function loadEvent() {
  if (eventId.value === null) {
    event.value = null
    return
  }

  try {
    const response = await api.get<EventData>(`/events/event/${eventId.value}/`)
    event.value = response.data
  } catch (error) {
    console.error('Errore caricamento evento:', error)
    event.value = null
  }
}

const empty = computed(() => !loading.value && posts.value.length === 0)

async function loadPosts(page = 1) {
  if (eventId.value === null) {
    posts.value = []
    totalCount.value = 0
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    const response = await api.get('/events/post/', {
      params: {
        event: eventId.value,
        page: page
      }
    })

    if (response.data.results) {
      posts.value = response.data.results
      totalCount.value = response.data.count
    } else {
      posts.value = response.data
      totalCount.value = response.data.length
    }

    currentPage.value = page
  } catch (error) {
    console.error('Errore caricamento post:', error)
    errorMessage.value = 'Impossibile caricare i post.'
  } finally {
    loading.value = false
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    loadPosts(page)
  }
}

function removePost(id: number) {
  posts.value = posts.value.filter(post => post.id !== id)
  loadPosts(currentPage.value)
}

function updatePost(updated: Post) {
  const index = posts.value.findIndex(post => post.id === updated.id)
  if (index !== -1) {
    posts.value[index] = updated
  }
}

function onPostCreated(newPost: Post) {
  isCreating.value = false
  loadPosts(1)
}

watch(eventId, () => {
  currentPage.value = 1
  loadPosts(1)
  loadEvent()
}, { immediate: true })
</script>

<template>
  <section class="max-w-4xl mx-auto p-4">
    <div class="grid grid-cols-3 items-center mb-6">
      <button 
        @click="isCreating = true" 
        class="w-15 text-3xl rounded-xs border border-[#8594E4] bg-white px-5 py-2 font-medium text-[#4C5DB2] shadow-sm hover:bg-[#8594E4] hover:text-white">+</button>
      <h1 class="text-center text-3xl font-bold tracking-tight text-heading md:text-4xl">
        {{ event?.title ?? 'Caricamento evento...' }}
      </h1>
    </div>

    <p v-if="loading" class="text-gray-500 text-center">Caricamento...</p>
    <p v-if="errorMessage" role="alert" class="text-red-500 text-center">
      {{ errorMessage }}
    </p>
    <p v-if="empty" class="text-gray-500 text-center">Non ci sono post per questo evento.</p>

    <!-- Post list -->
    <div class="space-y-4">
      <PostCard 
        v-for="post in posts" 
        :key="post.id" 
        :post="post" 
        @deleted="removePost" 
        @updated="updatePost"
      />
    </div>

    <nav v-if="totalCount > 0" aria-label="Page navigation" class="flex justify-center my-6">
      <ul class="flex -space-x-px text-sm select-none">
        <li>
          <button 
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            :class="[
              'flex items-center justify-center font-medium rounded-s-xl text-sm px-3 h-9 border transition-colors',
              currentPage === 1 
                ? 'opacity-40 cursor-not-allowed bg-gray-100 text-gray-400 border-gray-300' 
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
            ]"
          >
            Previous
          </button>
        </li>

        <li v-for="page in totalPages" :key="page">
          <button 
            @click="goToPage(page)"
            :class="[
              'flex items-center justify-center font-medium text-sm w-9 h-9 border transition-colors',
              currentPage === page
                ? 'bg-[#8594E4] text-white border-[#8594E4] font-bold shadow-sm'
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100 hover:text-black'
            ]"
          >
            {{ page }}
          </button>
        </li>

        <li>
          <button 
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage >= totalPages"
            :class="[
              'flex items-center justify-center font-medium rounded-e-xl text-sm px-3 h-9 border transition-colors',
              currentPage >= totalPages 
                ? 'opacity-40 cursor-not-allowed bg-gray-100 text-gray-400 border-gray-300' 
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
            ]"
          >
            Next
          </button>
        </li>
      </ul>
    </nav>

    <p v-if="totalCount > 0" class="text-center text-sm text-gray-500 mb-4">
      Pagina {{ currentPage }} di {{ totalPages }} ({{ totalCount }} post totali)
    </p>

    <div v-if="isCreating" class="modal-overlay">
      <PostForm 
        :event-id="eventId" 
        :post="null" 
        @saved="onPostCreated" 
        @cancel="isCreating = false"
      />
    </div>
  </section>
</template>