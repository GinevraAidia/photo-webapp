<template>
    <div id="event-header">
        <button id="new-event-btn" @click="isCreating=true"><span class="plus">+</span></button>
        <h1>Posts </h1>
    </div>
    <p v-if="empty">Non ci sono post per questo evento</p>
    <div>
        <PostCard v-for="post in posts" :key="post.id" :id="post.id" :uploader="post.username_utente" :description="post.description" :image="post.image"></PostCard>
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
