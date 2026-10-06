<template>
    <div class="cardEvent">
        <div @click="gestisciClick()" >
                <div class="card-title"><h1>{{titolo}}</h1></div>
                <div class="card-description"><p>{{ descrizione }}</p></div>
                <div class="card-text"><p>{{ visibilita }}</p></div>
        </div>
        <div class="card-buttons">
                <button @click="modificaEvent">Modifica</button>
                <button @click="eliminaEvent">Elimina</button>
        </div>
    </div>
    <div v-if="isModifying" class="modal-overlay">
    <div class="event-form" @click.stop>

        <button class="close-btn" @click="closeForm">×</button>

        <h2>Modifica evento</h2>

        <form @submit.prevent="salvaModifica">

            <input
                type="text"
                placeholder="Titolo"
                v-model="editTitle"
            >

            <input
                type="text"
                placeholder="Descrizione"
                v-model="editDescription"
            >

            <select v-model="editVisibility">
                <option disabled value="">
                    Seleziona la visibilità
                </option>

                <option value="public">
                    Pubblico
                </option>

                <option value="private">
                    Privato
                </option>
            </select>

            <span>Seleziona gli utenti</span>

            <select v-model="usernameChosen" @change="addUserToList">
                <option disabled :value="null">
                    Seleziona un utente
                </option>

                <option
                    v-for="user in users"
                    :key="user.id"
                    :value="user.id"
                >
                    {{ user.username }}
                </option>
            </select>

            <div v-if="editUsers.length > 0">
                <p>Utenti selezionati:</p>

                <ul>
                    <li
                        v-for="userId in editUsers"
                        :key="userId"
                    >
                        {{ getUsername(userId) }}
                    </li>
                </ul>
            </div>

            <button type="submit">
                Salva modifiche
            </button>

        </form>

    </div>
</div>

</template>
<script setup lang="ts">
import router from '@/router';
import api from '@/services/api';
import {ref} from 'vue'
const isModifying = ref(false)

const editTitle = ref('')
const editDescription = ref('')
const editVisibility = ref('')

const usernameChosen = ref<number | null>(null)

const editUsers = ref<number[]>([])
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
function gestisciClick() {
    router.push({ path: '/posts', query: { event: String(props.eventId) } })
}
function modificaEvent() {
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

}
</script>
