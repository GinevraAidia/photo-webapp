<template>
    <div id="event-header">
        <button id="new-event-btn" @click="isCreating=true"><span class="plus">+</span></button>
        <h1>Eventi</h1>
    </div>
    <div class="cards-container">
        <EventCard v-for="event in events" :key="event.id" :eventId="event.id" :titolo="event.title" :descrizione="event.description" :visibilita="event.visibility" :eventUsers="event.users" :users="users"></EventCard>
    </div>
    <div v-if="isCreating" class="modal-overlay">
        <div class="event-form" @click.stop>
            <button class="close-btn" @click="closeForm">×</button>
            <h2>Nuovo evento</h2>
            <form @submit.prevent="addEvent" >
                <input type="text" placeholder="Titolo" v-model="title" >
                <input type="text" placeholder="Descrizione" v-model="description">
                <select v-model="visibility">
                    <option disabled value="">Seleziona la visibilità</option>
                    <option value="public">Pubblico</option>
                    <option value="private">Privato</option>
                </select>
                <span>Seleziona gli utenti</span>
                <select v-model="usernameChosen"  @change="AddUserToList()" >
                    <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
                </select>
                <div v-if="userChosen.length > 0">
                    <p>Utenti selezionati:</p>
                    <ul>
                        <li v-for="userId in userChosen" :key="userId">
                            {{ users.find(user => user.id === userId)?.username }}
                        </li>
                    </ul>
                </div>
                <button type="submit">Aggiungi Evento</button>
            </form>
            
        </div>
        
    </div> 
</template>
<script setup lang="ts">
import {ref,onMounted} from 'vue'
import api from '@/services/api'
import EventCard from '@/components/EventCard.vue'

interface Event {
  id: number
  title: string
  description: string
  visibility: string
  users:number[]
}
interface User{
    id: number
    username: string
    email: string
}
const isCreating=ref(false)
const usernameChosen=ref<number | null>(null)
const visibility=ref('')
const title=ref('')
const description=ref('')
const users=ref<User[]>([])
const userChosen= ref<number[]>([])
const events = ref<Event[]>([])
async function getEvents(){
    const response = await api.get('/events/event/')
    events.value = response.data.results ?? response.data
} 
async function AddUserToList(){
    if (usernameChosen.value !== null && !userChosen.value.includes(usernameChosen.value)) {
        userChosen.value.push(usernameChosen.value)
    }
}
async function getUsers(){
    const response = await api.get('events/users/')
    users.value = response.data.results ?? response.data
}
async function addEvent(){
    const newEvent=ref({
        title:title.value,
        description:description.value,
        visibility:visibility.value,
        users:userChosen.value
    })
    try{
        const response = await api.post('/events/event/',newEvent.value)
        console.log(response.data)
        closeForm()
        getEvents()
    }catch(error){
        console.error(error)
    }
}
async function closeForm() {
    isCreating.value = false
    usernameChosen.value = null
    visibility.value = ''
    title.value = ''
    description.value = ''
    userChosen.value = []
}

onMounted(async()=>{
    getEvents()
    getUsers()
})
</script>