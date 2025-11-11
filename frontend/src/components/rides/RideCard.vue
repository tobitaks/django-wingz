<script setup>
import { computed } from 'vue'
import Badge from '../common/Badge.vue'
import { MapPinIcon, ClockIcon, UserIcon } from '@heroicons/vue/24/outline'
import dayjs from 'dayjs'

const props = defineProps({
  ride: {
    type: Object,
    required: true
  }
})

const statusVariant = computed(() => {
  const variants = {
    'en-route': 'info',
    'pickup': 'warning',
    'dropoff': 'success'
  }
  return variants[props.ride.status] || 'default'
})

const statusText = computed(() => {
  const texts = {
    'en-route': 'En Route',
    'pickup': 'Pickup',
    'dropoff': 'Dropoff'
  }
  return texts[props.ride.status] || props.ride.status
})

const formattedPickupTime = computed(() => {
  return dayjs(props.ride.pickup_time).format('MMM D, YYYY h:mm A')
})

const todayEventsCount = computed(() => {
  return props.ride.todays_ride_events?.length || 0
})
</script>

<template>
  <div class="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6">
    <!-- Header -->
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          Ride #{{ ride.id_ride }}
        </h3>
        <Badge :text="statusText" :variant="statusVariant" class="mt-1" />
      </div>
      <div v-if="todayEventsCount > 0" class="text-sm">
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {{ todayEventsCount }} event{{ todayEventsCount !== 1 ? 's' : '' }} today
        </span>
      </div>
    </div>

    <!-- Rider Info -->
    <div class="mb-3">
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <UserIcon class="w-4 h-4" />
        <span class="font-medium">Rider:</span>
        <span>{{ ride.rider.first_name }} {{ ride.rider.last_name }}</span>
      </div>
      <div class="ml-6 text-sm text-gray-500">
        {{ ride.rider.email }}
      </div>
    </div>

    <!-- Driver Info -->
    <div class="mb-3">
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <UserIcon class="w-4 h-4" />
        <span class="font-medium">Driver:</span>
        <span>{{ ride.driver.first_name }} {{ ride.driver.last_name }}</span>
      </div>
      <div class="ml-6 text-sm text-gray-500">
        {{ ride.driver.email }}
      </div>
    </div>

    <!-- Pickup Time -->
    <div class="mb-3">
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <ClockIcon class="w-4 h-4" />
        <span class="font-medium">Pickup:</span>
        <span>{{ formattedPickupTime }}</span>
      </div>
    </div>

    <!-- Location -->
    <div>
      <div class="flex items-start gap-2 text-sm text-gray-600">
        <MapPinIcon class="w-4 h-4 mt-0.5 flex-shrink-0" />
        <div>
          <div class="font-medium">Pickup Location:</div>
          <div class="text-gray-500">
            {{ ride.pickup_latitude.toFixed(4) }}, {{ ride.pickup_longitude.toFixed(4) }}
          </div>
          <div class="font-medium mt-1">Dropoff Location:</div>
          <div class="text-gray-500">
            {{ ride.dropoff_latitude.toFixed(4) }}, {{ ride.dropoff_longitude.toFixed(4) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
