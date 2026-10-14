<template>
    <div class="cardEvent">
        <div @click="gestisciClick()" >
                <div class="rounded-full border border-dashed border-indigo-300
         bg-indigo-50/40 px-5 py-3
         hover:border-[1.5px] hover:border-[#df73ff]"><h1>{{titolo}}</h1></div>
                <div class="card-description,max-w-xs truncate px-6 py-4 text-gray-600"><p>{{ descrizione }}</p></div>
                <div class="card-text"><p><span :class="visibilita === 'public' ? 'bg-green-100 text-green-700': 'bg-purple-100 text-purple-700'" class="rounded-full px-3 py-1 text-xs font-medium">{{ visibilita === 'public' ? 'Pubblico' : 'Privato' }}
      </span></p></div>
        </div>
        <div class="card-buttons">
                <button @click="emit('edit', eventId)">Modifica</button>
                <button @click="emit('delete', eventId)">Elimina</button>
        </div>
    </div>

</template>
<script setup lang="ts">
import router from '@/router';
/* import api from '@/services/api';
import {ref} from 'vue' */
/* const isModifying = ref(false)

const editTitle = ref('')
const editDescription = ref('')
const editVisibility = ref('')

const usernameChosen = ref<number | null>(null)

const editUsers = ref<number[]>([]) */
interface User {
    id: number
    username: string
    email: string
}

const props = defineProps<{
    eventId: number
    titolo: string
    descrizione: string
    visibilita: string
    eventUsers: number[]
    users: User[]
}>()
const emit = defineEmits<{
  edit: [id: number]
  delete: [id: number]
}>()

function gestisciClick() {
    router.push({ path: '/posts', query: { event: String(props.eventId) } })
}
/* function modificaEvent() {
    editTitle.value = props.titolo
    editDescription.value = props.descrizione
    editVisibility.value = props.visibilita

    // Copia gli utenti già presenti nell'evento
    editUsers.value = [...props.eventUsers]

    usernameChosen.value = null

    isModifying.value = true
}

function addUserToList() {
    if (
        usernameChosen.value !== null &&
        !editUsers.value.includes(usernameChosen.value)
    ) {
        editUsers.value.push(usernameChosen.value)
    }
}
function getUsername(userId: number) {
    return props.users.find(
        user => user.id === userId
    )?.username
}
async function salvaModifica() {
    try {
        await api.patch(
            `/events/event/${props.eventId}/`,
            {
                title: editTitle.value,
                description: editDescription.value,
                visibility: editVisibility.value,
                users: editUsers.value
            }
        )


    } catch (error) {
        console.error(error)
    }
    
    closeForm()

    window.location.reload()
} 
 function closeForm() {
    isModifying.value = false

    editTitle.value = ''
    editDescription.value = ''
    editVisibility.value = ''

    usernameChosen.value = null
    editUsers.value = []
}

async function eliminaEvent() {
    alert("Sicuro di voler eliminare l'evento? verranno eliminati anche tutti i post associati.\n Attenzione solo il proprietario dell'evento è autorizzato a farlo")
    try{
        await api.delete(`/events/event/${props.eventId}/`)
        window.location.reload()
    }catch(error){
        console.log(error)
        alert("Errore durante l'eliminazione dell'evento")
    }

}  */
</script>
