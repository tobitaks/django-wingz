<script setup>
import { XCircleIcon, XMarkIcon } from '@heroicons/vue/24/outline'

defineProps({
  message: {
    type: String,
    required: true
  },
  dismissible: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['dismiss'])
</script>

<template>
  <div class="bg-red-50 border border-red-200 rounded-lg p-4">
    <div class="flex items-start gap-3">
      <XCircleIcon class="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
      <div class="flex-1">
        <p class="text-sm text-red-800">{{ message }}</p>
      </div>
      <button
        v-if="dismissible"
        @click="emit('dismiss')"
        class="text-red-600 hover:text-red-800"
      >
        <XMarkIcon class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>
