<script setup>
import AppHeader from './AppHeader.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <AppHeader />

    <!-- Main Content -->
    <main class="flex-1 p-6">
      <slot />
    </main>
  </div>
</template>

<style scoped>
/* Layout styles */
</style>
