<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

import PostCard from '@/components/PostCard.vue'
import PostForm from '@/components/PostForm.vue'
import { postService } from '@/services/postService'
import type { Post, PostFormData } from '@/types/post'
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

async function createPost(data: PostFormData) {
  if (eventId.value === null) return

  loading.value = true

  try {
    const post = await postService.create(
      eventId.value,
      data
    )

    posts.value.push(post)
    isCreating.value = false
  } catch {
    errorMessage.value = 'Errore durante la creazione.'
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

    <PostCard
      v-for="post in posts"
      :key="post.id"
      :post="post"
      @deleted="removePost"
      @updated="updatePost"
    />

    <div v-if="isCreating" class="modal-overlay">
      <PostForm
        :loading="loading"
        submit-label="Crea post"
        @submit="createPost"
        @cancel="isCreating = false"
      />
    </div>
  </section>
</template>



<!-- <template>
    <div id="event-header">
        <button id="new-event-btn" @click="isCreating=true"><span class="plus">+</span></button>
        <h1>Posts </h1>
    </div>
    <p v-if="empty">Non ci sono post per questo evento</p>
    <div>
        <PostCard v-for="post in posts" :key="post.id" @deleted="removePost" :id="post.id" :uploader="post.username_utente" :description="post.description" :image="post.image"></PostCard>
    </div>
    <div v-if="isCreating" class="modal-overlay">
        <div class="event-form" @click.stop>
            <button class="close-btn" @click="closeForm">×</button>
            <h2>Nuovo Post</h2>
            <form @submit.prevent="addPost">
                <input type="text" placeholder="Descrizione" v-model="newPost.description">
                <input type="file" accept="image/*" @change="gestisciCaricamento">
                <button type="submit">Aggiungi POST</button>
            </form>
        </div>
        
    </div>
</template>
<script setup lang="ts">
import {ref,onMounted} from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import PostCard from '@/components/PostCard.vue'

interface Post {
  id: number
  username_utente: string
  description: string
  image: string
}
const isCreating=ref(false)
const route = useRoute()
const posts = ref<Post[]>([])
const newPost = ref({
    description:'',
    image: null as File | null,
    event: route.query.event
})
const empty=ref(false)
async function getPosts(){
    const response = await api.get('/events/post/', {
        params: { event: route.query.event }
    })
    posts.value = response.data.results ?? response.data
    if(response.data.results.length==0){
        empty.value=true
    }
}
async function addPost(){
    try {
        const formData = new FormData()
        formData.append('event', String(newPost.value.event))
        formData.append('description', newPost.value.description)
        if (newPost.value.image instanceof File) {
            formData.append('image', newPost.value.image)
        }

        const response = await api.post('/events/post/', formData)
        console.log(response)
        await getPosts()
        closeForm()
    } catch (error) {
        console.error(error)
    }
}
function removePost(id: number) {
  posts.value = posts.value.filter(
    post => post.id !== id
  )
}
const gestisciCaricamento = (event:any) => {
  const file = event.target.files[0]
  if (!file) return

  newPost.value.image = file
}
async function closeForm() {
    isCreating.value = false
    newPost.value.description = ''
    newPost.value.image = null
}
onMounted(async()=>{
    getPosts()
}) 
</script>
 -->