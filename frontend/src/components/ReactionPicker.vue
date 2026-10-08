<script setup lang="ts">
import { ref } from 'vue'
import type { Emoji } from '@/types/post'

const emit = defineEmits<{
  selected: [emoji: Emoji]
}>()

const selected = ref<Emoji | ''>('')

function onChange() {
  if (selected.value) {
    emit('selected', selected.value)
  }
}
</script>

<template>
  <select v-model="selected" @change="onChange">
    <option value="" disabled>Reagisci</option>
    <option value="like">👍</option>
    <option value="dislike">👎</option>
    <option value="heart">❤️</option>
    <option value="laugh">😂</option>
  </select>
</template>