<script setup>
import { ref } from 'vue'
import { Bars3Icon } from '@heroicons/vue/24/outline'

defineProps({
  sidebarOpen: Boolean
})

const emit = defineEmits(['toggle-sidebar'])
</script>

<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="px-4 py-4 flex items-center justify-between">
      <!-- Logo and Menu Toggle -->
      <div class="flex items-center gap-4">
        <button
          @click="emit('toggle-sidebar')"
          class="lg:hidden p-2 rounded-md hover:bg-gray-100"
        >
          <Bars3Icon class="w-6 h-6 text-gray-600" />
        </button>
        <h1 class="text-xl font-bold text-gray-900">
          Wingz Ride Management
        </h1>
      </div>

      <!-- User Info (placeholder) -->
      <div class="flex items-center gap-3">
        <span class="text-sm text-gray-600 hidden sm:inline">Admin User</span>
        <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
          <span class="text-white text-sm font-medium">A</span>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* Header styles */
</style>
