<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const { username } = storeToRefs(userStore);

async function Modify() {
   
}
</script>

<template>
<form class="max-w-md mx-auto">
  <div class="relative z-0 w-full mb-5 group">
    <h2 >Username:{{ username}}</h2>  
    <button >Modifica</button>
  </div>
  <div class="relative z-0 w-full mb-5 group">
    <h2>Email:</h2>  
    <button >Modifica</button>
    </div>
</form>

</template>