<script lang="ts" setup>
import UserForm from '@/components/UserForm.vue';

</script>

<template>
    <div class="mx-auto flex max-w-sm items-center gap-x-4 rounded-xl bg-white p-6 shadow-lg outline ">
        <svg class="w-6 h-6 mb-1 text-body group-hover:text-fg-brand" aria-hidden="true" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0 0a8.949 8.949 0 0 0 4.951-1.488A3.987 3.987 0 0 0 13 16h-2a3.987 3.987 0 0 0-3.951 3.512A8.948 8.948 0 0 0 12 21Zm3-11a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"></path></svg>
        <h1>UserProfile</h1>
    </div>
    <div class="m-auto content-center max-w-sm items-center gap-x-4">
            <UserForm/>
    </div>
</template>

