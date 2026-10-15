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
</script>
