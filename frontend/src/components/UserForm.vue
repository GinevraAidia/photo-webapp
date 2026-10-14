<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
const auth=useAuthStore()
</script>

<template>
    <p>form</p>
    <div >
        <form>
            <h2>Username:</h2>
            <h2>Email:</h2>
        </form> 
    </div>
</template>