<template>
    <div class="login-view">
        <LoginForm/>
    </div>
</template>
<script setup lang="ts">
import LoginForm from '@/components/LoginForm.vue';

</script>

<style>
.login-view {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding-top: 20px;
    box-sizing: border-box;
}
</style>

