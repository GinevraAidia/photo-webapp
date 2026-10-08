<script setup lang="ts">
import type { PostReaction } from '@/types/post'

defineProps<{
  reactions: PostReaction[]
}>()
</script>

<template>
   <div class="reaction-list">
    <div
      v-for="reaction in reactions"
      :key="reaction.id"
      class="reaction-item"
    >
      <span>{{ reaction.username_utente }}</span>
      <span>{{ reaction.reaction_symbol }}</span>
    </div>
  </div>
</template>