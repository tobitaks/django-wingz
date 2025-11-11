<script setup>
import { InboxIcon } from '@heroicons/vue/24/outline'

defineProps({
  title: {
    type: String,
    default: 'No data found'
  },
  message: {
    type: String,
    default: 'There are no items to display.'
  }
})
</script>

<template>
  <div class="text-center py-12">
    <InboxIcon class="w-12 h-12 mx-auto text-gray-400 mb-4" />
    <h3 class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-sm text-gray-500">{{ message }}</p>
  </div>
</template>
