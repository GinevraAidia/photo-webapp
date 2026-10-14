<template>
    <div id="event-header">
        <button id="new-event-btn" class="rounded-xl border border-[#8594E4]
         bg-white px-5 py-2
         font-medium text-[#4C5DB2]
         shadow-sm
         hover:bg-[#8594E4] hover:text-white
         hover:shadow-md
         transition-all duration-300" @click="isCreating=true"><span class="plus">+</span></button>
        <h1>Eventi</h1>
        <div >
            <label class="inline-flex items-center cursor-pointer">
            <span class="select-none me-3 text-sm font-medium text-heading">Card</span>
            <input type="checkbox" v-model="isToggled" value="" class="sr-only peer">
            <div class="relative w-9 h-5 bg-neutral-quaternary rounded-full peer dark:bg-blue-200 peer-focus:ring-4 peer-focus:ring-purple-100 dark:peer-focus:ring-purple-100 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-purple-300 dark:peer-checked:bg-purple-300"></div>
            <span class="select-none ms-3 text-sm font-medium text-heading">Table</span>
            </label>
        </div>
    </div>
    <div class="flex items-center max-w-lg mx-auto space-x-2">   
          <label for="voice-search" class="sr-only">Search</label>
          <div class="relative w-full">
              <input type="text" id="voice-search" v-model="searchQuery" class="block w-full ps-9 pe-3 py-2.5 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand shadow-xs placeholder:text-body" placeholder="Search Title or Description" required />
          </div>
        </div>
    <div v-if="!isToggled" class="cards-container">
        <EventCard class="card"
            v-for="event in filteredEvents"
            :key="event.id"
            :eventId="event.id"
            :titolo="event.title"
            :descrizione="event.description"
            :visibilita="event.visibility"
            :eventUsers="event.users"
            :users="users"
            @edit="id => {
                const event = events.find(e => e.id === id)
                if (event) editEvent(event)
            }"
            @delete="deleteEvent"
            />
    </div>
    <div v-if="isToggled" class="table-container">
        <EventTable :events="filteredEvents" @delete="deleteEvent" @edit="editEvent" />
    </div>
    <EventForm
        v-if="isCreating || editingEvent"
        :key="editingEvent?.id ?? 'new'"
        :event="editingEvent"
        :users="users"
        @cancel="closeForm"
        @submit="saveEvent"
        />
</template>
<script setup lang="ts">
import {ref,onMounted,computed} from 'vue'
import api from '@/services/api'
import EventCard from '@/components/EventCard.vue'
import { eventService } from '@/services/eventService'
import EventTable from '@/components/EventTable.vue'
import type { Event, EventFormData } from '@/types/post'
import EventForm from '@/components/EventForm.vue'

const editingEvent = ref<Event | null>(null)
const isToggled = ref(false)

const searchQuery = ref('');

interface User{
    id: number
    username: string
    email: string
}
const isCreating=ref(false)
const users=ref<User[]>([])
const events = ref<Event[]>([])
async function getEvents(){
    const response = await api.get('/events/event/')
    events.value = response.data.results ?? response.data
} 
async function getUsers(){
    const response = await api.get('events/users/')
    users.value = response.data.results ?? response.data
}

function closeForm() {
  isCreating.value = false
  editingEvent.value = null
}
async function deleteEvent(id: number) {
  try {
    await eventService.delete(id)
    events.value = events.value.filter(event => event.id !== id)
  } catch (error) {
    console.error('Errore eliminazione evento:', error)
  }
}
function editEvent(event: Event) {
  isCreating.value = false
  editingEvent.value = event
}
async function saveEvent(data: EventFormData) {
  console.log('Dati inviati:', data)

  try {
    if (editingEvent.value) {
      await eventService.update(editingEvent.value.id, data)
    } else {
      await eventService.create(data)
    }

    await getEvents()
    closeForm()
  } catch (error) {
    console.error('Errore salvataggio evento:', error)
  }
}
const filteredEvents= computed<Event[]>(()  => {
  console.log(searchQuery.value)
  return events.value.filter((event: { title: string | string[]; description: string | string[] }) => event.title.includes(searchQuery.value) || event.description.includes(searchQuery.value))
})
onMounted(async()=>{
    getEvents()
    getUsers()
})
</script>