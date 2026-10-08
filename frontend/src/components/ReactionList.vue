<script setup lang="ts">
import type { Reaction, Emoji } from '@/types/post'

defineProps<{
  reactions: Reaction[]
}>()

const emojiMap: Record<Emoji, string> = {
  like: '👍',
  dislike: '👎',
  heart: '❤️',
  laugh: '😂'
}
</script>

<template>
   <div class="reaction-list">
    <div
      v-for="reaction in reactions"
      :key="reaction.id"
      class="reaction-item"
    >
      <span>{{ reaction.username_utente }}</span>
      <span>{{ emojiMap[reaction.emoji] }}</span>
    </div>
  </div>
</template>