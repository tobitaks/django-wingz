<script setup>
defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-8 h-8',
  lg: 'w-12 h-12'
}
</script>

<template>
  <div class="flex items-center justify-center">
    <div
      :class="[
        'animate-spin rounded-full border-2 border-gray-300 border-t-blue-600',
        sizeClasses[size]
      ]"
    ></div>
  </div>
</template>
