
<template>
  <div id="container">
    <AppBar></AppBar>
    <RouterView />
  </div>
  
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import { ref } from 'vue';
import AppBar from './components/AppBar.vue';
import './styles/main.css';
import '@/styles/gridCard.css'
const isVisible = ref(true);
</script>

<style scoped>
h1{
  text-align: center;
}
#container{
  padding-top: 100px;
  justify-content: center;
  flex: auto;
}
</style>
