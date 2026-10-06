<template>
    <div class="cardPost">
        <img v-if="image" :src="image" :alt="title" />
        <div class="card-title">
            <h1 >{{description}}</h1>
        </div>
        <div class="card-text">
            <p >{{ uploader }}</p>
        </div>
        <div class="card-buttons">
            <select v-model="scelta" @change="react(props.id)">
                <option value="" disabled selected>Scegli una reazione</option>
                <option value="like">👍</option>
                <option value="dislike">👎</option>
                <option value="heart">❤️</option>
                <option value="laugh">😂</option>
            </select>
            <div v-for="reaction in reactions">
                <p>{{reaction.username_utente}}:{{ emojiMap[reaction.emoji] }}</p>
            </div>
            <button @click="mostraModificaForm()">Modifica</button>
            <button @click="eliminaPost">Elimina</button>
        </div>
    </div>
    <div v-if="isModifing" class="modal-overlay">
        <div class="event-form" @click.stop>
            <button class="close-btn" @click="closeForm">×</button>
            <h2>Modifica Post</h2>
            <form @submit.prevent="modificaPost">
                <input type="text" placeholder="Descrizione" v-model="oldPost.description">
                <input type="file" accept="image/*" @change="gestisciCaricamento">
                <button type="submit">Modifica POST</button>
            </form>
        </div> 
    </div>

</template>
<script setup lang="ts">
import api from '@/services/api';
import {ref,onMounted} from 'vue'
import { useRoute } from 'vue-router'


const scelta = ref('')
const emojiMap: Record<string, string> = {
    like: "👍",
  dislike: "👎",
  heart: "❤️",
  laugh: "😂"
}
interface Post {
  id: number
  title: string
  uploader: number
  description: string
  image: string
}

interface Reaction {
    id: number
    post: number
    username_utente: string
    emoji: string
}
const reactions = ref<Reaction[]>([])
const props=defineProps({
    id:Number,
    title: String,
    uploader: String,
    description: String,
    image: String
})
const isModifing = ref(false)
const oldPost = ref({
    description: '',
    image: null as File | null,
    event: null as number | null
})
async function getReactions(){
    const response = await api.get('/events/reaction/', {
        params: { post: props.id }
    })
    reactions.value = response.data.results ?? response.data
}
async function react(title: any){
    const postData= ( {
        post:props.id,
        emoji:scelta.value
    })
    try{
        const response = await api.post('/events/reaction/',postData)
        console.log(response.data)
        getReactions()
    }catch(error){
        console.error(error)
    }
}
async function modificaPost(){
    alert("Attenzione solo il proprietario dell'evento è autorizzato a modificarlo")
    const formData=new FormData()
    formData.append('description',oldPost.value.description)
    if(oldPost.value.image){
        formData.append('image',oldPost.value.image)
    }
    try{
        const response = await api.patch(`/events/post/${props.id}/`,formData,{
            headers:{
                'Content-Type':'multipart/form-data'
            }
        })
        console.log(response.data)
        window.location.reload()
    }catch(error){
        console.error(error)
    }
    closeForm()
    window.location.reload()
}

async function eliminaPost() {
    alert("Sicuro di voler eliminare il post? verranno eliminati anche tutte le reazioni associate.\n Attenzione solo il proprietario dell'evento è autorizzato a farlo")
    try{
        await api.delete(`/events/post/${props.id}/`)
        window.location.reload()
    }catch(error){
        console.log(error)
        alert("Errore durante l'eliminazione del post")
    }

}
async function mostraModificaForm() {
    oldPost.value.description = props.description ?? ''
    oldPost.value.image = null

    isModifing.value = true
    
}
async function closeForm() {
    isModifing.value = false
    
}
function gestisciCaricamento(event: Event) {
    const input = event.target as HTMLInputElement
    const file = input.files?.[0]

    if (file) {
        oldPost.value.image = file
    }
}


onMounted(async()=>{
    getReactions()
})
</script>