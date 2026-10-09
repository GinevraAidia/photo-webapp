<template>
  <tr class="transition-colors hover:bg-gray-50 text-center" @click="gestisciClick()">

    <td class="px-6 py-4 font-medium text-gray-900 text-center">
      {{ event.title }}
    </td>

    <td class="max-w-xs truncate px-6 py-4 text-gray-600 text-center">
      {{ event.description }}
    </td>

    <td class="px-6 py-4 text-center">
      <span
        :class="event.visibility === 'public'
          ? 'bg-green-100 text-green-700'
          : 'bg-purple-100 text-purple-700'"
        class="rounded-full px-3 py-1 text-xs font-medium text-center"
      >
        {{ event.visibility === 'public' ? 'Pubblico' : 'Privato' }}
      </span>
    </td>

    <td class="px-6 py-4 flex justify-center text-center">
        <button type="button" class="rounded-lg p-2 hover:bg-gray-200 " @click.stop="toggleMenu">
            ⋮
        </button>
    </td>
    
  </tr>
  <Teleport to="body">
  <div
    v-if="menuOpen"
    class="fixed z-[9999] w-40 rounded-lg border border-gray-200 bg-white py-1 shadow-lg"
    :style="{
      top: `${menuTop}px`,
      left: `${menuLeft}px`
    }"
  >
    <button
      type="button"
      class="block w-full px-4 py-2 text-left hover:bg-gray-100"
      @click="emit('edit', event); menuOpen = false"
    >
      ✏️ Modifica
    </button>

    <button
      type="button"
      class="block w-full px-4 py-2 text-left text-red-600 hover:bg-red-50"
      @click="emit('delete', event.id); menuOpen = false"
    >
      🗑️ Elimina
    </button>
  </div>
</Teleport>
</template>
<script setup lang="ts">
import router from '@/router';
import type{Event} from '@/types/post'
import {ref} from 'vue'
const props=defineProps<{
  event: Event
}>()

const emit = defineEmits<{
  delete: [id: number]
  edit: [event: Event]
}>()

const menuOpen = ref(false)
const menuTop = ref(0)
const menuLeft = ref(0)

function toggleMenu(e: MouseEvent) {
  const button = e.currentTarget as HTMLButtonElement
  const rect = button.getBoundingClientRect()

  menuTop.value = rect.bottom + 4
  menuLeft.value = Math.max(8, rect.right - 160)

  menuOpen.value = !menuOpen.value
}
function gestisciClick() {
    router.push({ path: '/posts', query: { event: String(props.event.id) } })
}
</script>