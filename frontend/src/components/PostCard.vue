<template>
  <article class="cardPost">
    <img
      v-if="post.image"
      :src="post.image"
      alt="Immagine del post"
    />

    <h2>{{ post.description }}</h2>
    <p>{{ post.username_utente }}</p>

    <ReactionPicker @selected="react" />

    <ReactionList :reactions="reactions" />

    <button @click="editing = true">
      Modifica
    </button>

    <button @click="deletePost">
      Elimina
    </button>

    <p v-if="errorMessage" role="alert">
      {{ errorMessage }}
    </p>

    <div v-if="editing" class="modal-overlay">
      <PostForm
        :key="post.id"
        :post="post"
        @saved="post => emit('updated', post)"
        @cancel="editing = false"
      />
    </div>
  </article>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Post, PostReaction } from '@/types/post'

import PostForm from './PostForm.vue'
import ReactionPicker from './ReactionPicker.vue'
import ReactionList from './ReactionList.vue'

import { postService } from '@/services/postService'
import { reactionService } from '@/services/reactionService'

const props = defineProps<{
  post: Post
}>()

const emit = defineEmits<{
  deleted: [id: number]
  updated: [post: Post]
}>()

const reactions = ref<PostReaction[]>([])
const editing = ref(false)
const errorMessage = ref('')

async function loadReactions() {
  reactions.value = await reactionService.getByPost(
    props.post.id
  )
}

async function react(reactionId: number) {
  try {
    await reactionService.setReaction(props.post.id, reactionId)
    await loadReactions()
  } catch {
    errorMessage.value = 'Impossibile salvare la reazione.'
  }
}

async function deletePost() {
  if (!window.confirm('Eliminare questo post?')) {
    return
  }

  try {
    await postService.delete(props.post.id)
    emit('deleted', props.post.id)
  } catch {
    errorMessage.value = 'Errore durante l’eliminazione.'
  }
}

onMounted(loadReactions)
</script>
