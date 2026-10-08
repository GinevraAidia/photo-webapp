<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { ReactionType } from '@/types/post'
import { reactionService } from '@/services/reactionService'

const emit = defineEmits<{
  selected: [reactionId:number]
}>()

const reactions= ref<ReactionType[]>([])
const selected = ref<number | ''>('')

function onChange() {
  if (selected.value) {
    emit('selected', selected.value)
  }
}
onMounted(async () => {
  reactions.value= await reactionService.getTypes()
  })
</script>

<template>
  <select v-model="selected" @change="onChange">
    <option value="" disabled>Reagisci</option>

    <option
      v-for="reaction in reactions"
      :key="reaction.id"
      :value="reaction.id"
    >
      {{ reaction.symbol }}
    </option>
  </select>
</template>