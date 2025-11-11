<script setup>
import { ref } from 'vue'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'

const sidebarOpen = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <AppHeader
      :sidebar-open="sidebarOpen"
      @toggle-sidebar="toggleSidebar"
    />

    <div class="flex">
      <!-- Sidebar -->
      <AppSidebar
        :is-open="sidebarOpen"
        @close="closeSidebar"
      />

      <!-- Main Content -->
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Layout styles */
</style>
