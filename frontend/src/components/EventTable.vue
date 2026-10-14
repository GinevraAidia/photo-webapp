<template>
    <div class="w-full overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-sm mt-5">

    <table class="w-full min-w-[650px] text-sm">

      <thead class="bg-gray-100 text-xs uppercase text-gray-600">
        <tr>
          <th class="px-6 py-4 font-semibold text-center">Title</th>
          <th class="px-6 py-4 font-semibold text-center">Description</th>
          <th class="px-6 py-4 font-semibold text-center">Visibility</th>
          <th class="px-6 py-4 font-semibold text-center">Actions</th>
        </tr>
      </thead>

      <tbody class="divide-y divide-gray-200">
        <EventRow
            v-for="event in events"
            :key="event.id"
            :event="event"
            @delete="emit('delete', $event)"
            @edit="emit('edit', $event)"
            />
      </tbody>

    </table>

    <div
      v-if="events.length === 0"
      class="p-8 text-center text-gray-500"
    >
      Nessun evento disponibile.
    </div>
  </div>
</template>
<script setup lang="ts">
import EventRow from './EventRow.vue';
import type { Event } from '@/types/post.ts';
const props= defineProps<{
    events:Event[]
}>()
const emit = defineEmits<{
  delete: [id: number]
  edit: [event: Event]
}>()
</script>