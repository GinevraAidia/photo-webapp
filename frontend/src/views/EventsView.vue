<template>
  <div id="event-header">
    <button 
      id="new-event-btn" 
      class="rounded-xl border border-[#8594E4] bg-white px-5 py-2 font-medium text-[#4C5DB2] shadow-sm hover:bg-[#8594E4] hover:text-white hover:shadow-md transition-all duration-300" 
      @click="isCreating = true"
    >
      <span class="plus">+</span>
    </button>

    <h1>Eventi</h1>

    <div>
      <label class="inline-flex items-center cursor-pointer">
        <span class="select-none me-3 text-sm font-medium text-heading">Card</span>
        <input type="checkbox" v-model="isToggled" class="sr-only peer">
        <div class="relative w-9 h-5 bg-neutral-quaternary rounded-full peer dark:bg-blue-200 peer-focus:ring-4 peer-focus:ring-purple-100 dark:peer-focus:ring-purple-100 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-purple-300 dark:peer-checked:bg-purple-300"></div>
        <span class="select-none ms-3 text-sm font-medium text-heading">Table</span>
      </label>
    </div>
  </div>

  <div class="flex items-center max-w-lg mx-auto space-x-2 my-4">   
    <label for="voice-search" class="sr-only">Search</label>
    <div class="relative w-full">
      <input 
        type="text" 
        id="voice-search" 
        v-model="searchQuery" 
        class="block w-full px-4 py-2.5 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-xl focus:ring-[#8594E4] focus:border-[#8594E4] shadow-xs" 
        placeholder="Cerca per titolo o descrizione..." 
      />
      <button @click=filterEvents>Search</button>
    </div>
  </div>
    
  <nav aria-label="Page navigation" class="flex justify-center my-4">
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
          ]">Previous
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
          ]">{{ page }}
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
          ]">Next
        </button>
      </li>
    </ul>
  </nav>

  <p class="text-center text-sm text-gray-500 mb-4">
    Pagina {{ currentPage }} di {{ totalPages }} ({{ totalCount }} eventi totali)
  </p>
    
  <div v-if="!isToggled" id="event-container" class="cards-container">
    <EventCard 
      class="card"
      v-for="event in events"
      :key="event.id"
      :eventId="event.id"
      :titolo="event.title"
      :descrizione="event.description"
      :visibilita="event.visibility"
      :eventUsers="event.users"
      :users="users"
      @edit="id => {
        const found = events.find(e => e.id === id)
        if (found) editEvent(found)
      }"
      @delete="deleteEvent"
    />
  </div>
    
  <div v-if="isToggled" id="event-container" class="table-container">
    <EventTable :events="events" @delete="deleteEvent" @edit="editEvent" />
  </div>
    
  <EventForm
    v-if="isCreating || editingEvent"
    :key="editingEvent?.id ?? 'new'"
    :event="editingEvent"
    :users="users"
    @saved="() => getEvents(currentPage)"
    @cancel="closeForm"/>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/services/api'
import EventCard from '@/components/EventCard.vue'
import EventTable from '@/components/EventTable.vue'
import EventForm from '@/components/EventForm.vue'
import { eventService } from '@/services/eventService'
import type { Event } from '@/types/post'

interface User {
  id: number
  username: string
  email: string
}

const events = ref<Event[]>([])
const users = ref<User[]>([])
const editingEvent = ref<Event | null>(null)
const isCreating = ref(false)
const isToggled = ref(false)
const searchQuery = ref('')

const currentPage = ref(1)
const perPage = ref(6)
const totalCount = ref(0)

const totalPages = computed(() => {
  return Math.ceil(totalCount.value / perPage.value) || 1
})

async function getEvents(page: number) {
  try {
    const response = await api.get('/events/event/', {
      params: {
        page: page,
        search: searchQuery.value || undefined
      }
    })

    if (response.data.results) {
      events.value = response.data.results
      totalCount.value = response.data.count
    } else {
      events.value = response.data
      totalCount.value = response.data.length
    }
    currentPage.value = page
  } catch (error) {
    console.error('Errore nel recupero eventi:', error)
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    getEvents(page)
  }
}
//Da modificare per query a db
async function filterEvents() {
    /* events.value.filter(event => {
      return event.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
             event.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    }) */
   try{
    const response =await api.get('/events/event/', {
      params: {
        search: searchQuery.value
      }
    })
    events.value = response.data.results ?? response.data
    totalCount.value = response.data.count ?? response.data.length
   } catch (error) {
    console.error('Errore nel recupero eventi:', error)
   }
}

async function getUsers() {
  try {
    const response = await api.get('/events/users/')
    users.value = response.data.results ?? response.data
  } catch (error) {
    console.error('Errore nel recupero utenti:', error)
  }
}

function closeForm() {
  isCreating.value = false
  editingEvent.value = null
}

async function deleteEvent(id: number) {
  try {
    await eventService.delete(id)
    await getEvents(currentPage.value)
  } catch (error) {
    console.error('Errore eliminazione evento:', error)
  }
}

function editEvent(event: Event) {
  isCreating.value = false
  editingEvent.value = event
}

onMounted(() => {
  getEvents(1)
  getUsers()
})
</script>