<script setup>
import { ref, watch } from 'vue'
import { MagnifyingGlassIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      status: '',
      rider_email: '',
      ordering: '-pickup_time'
    })
  }
})

const emit = defineEmits(['update:modelValue', 'apply'])

const filters = ref({ ...props.modelValue })

const statusOptions = [
  { value: '', label: 'All Statuses' },
  { value: 'en-route', label: 'En Route' },
  { value: 'pickup', label: 'Pickup' },
  { value: 'dropoff', label: 'Dropoff' }
]

const sortOptions = [
  { value: '-pickup_time', label: 'Newest First' },
  { value: 'pickup_time', label: 'Oldest First' }
]

const applyFilters = () => {
  emit('update:modelValue', { ...filters.value })
  emit('apply')
}

const clearFilters = () => {
  filters.value = {
    status: '',
    rider_email: '',
    ordering: '-pickup_time'
  }
  applyFilters()
}

const hasActiveFilters = () => {
  return filters.value.status !== '' || filters.value.rider_email !== ''
}

// Debounce email search
let emailTimeout = null
watch(() => filters.value.rider_email, (newValue) => {
  clearTimeout(emailTimeout)
  emailTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
})
</script>

<template>
  <div class="bg-white rounded-lg shadow p-4">
    <div class="flex flex-col lg:flex-row gap-4">
      <!-- Status Filter -->
      <div class="flex-1">
        <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
          Status
        </label>
        <select
          id="status"
          v-model="filters.status"
          @change="applyFilters"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option v-for="option in statusOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Email Search -->
      <div class="flex-1">
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
          Rider Email
        </label>
        <div class="relative">
          <input
            id="email"
            v-model="filters.rider_email"
            type="text"
            placeholder="Search by email..."
            class="w-full px-3 py-2 pl-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <MagnifyingGlassIcon class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" />
        </div>
      </div>

      <!-- Sort By -->
      <div class="flex-1">
        <label for="sort" class="block text-sm font-medium text-gray-700 mb-1">
          Sort By
        </label>
        <select
          id="sort"
          v-model="filters.ordering"
          @change="applyFilters"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option v-for="option in sortOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Clear Button -->
      <div class="flex items-end">
        <button
          v-if="hasActiveFilters()"
          @click="clearFilters"
          class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md flex items-center gap-2 transition-colors"
        >
          <XMarkIcon class="w-4 h-4" />
          Clear
        </button>
      </div>
    </div>
  </div>
</template>
