<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRideStore } from '../stores/rideStore'
import MainLayout from '../components/layout/MainLayout.vue'
import Badge from '../components/common/Badge.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ErrorAlert from '../components/common/ErrorAlert.vue'
import RideFormModal from '../components/rides/RideFormModal.vue'
import { MapPinIcon, ClockIcon, UserIcon, TrashIcon, PencilIcon, ClipboardDocumentListIcon } from '@heroicons/vue/24/outline'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

const route = useRoute()
const router = useRouter()
const rideStore = useRideStore()

const ride = ref(null)
const loading = ref(true)
const error = ref(null)
const showDeleteConfirm = ref(false)
const deleting = ref(false)
const showEditModal = ref(false)

const rideId = computed(() => parseInt(route.params.id))

const statusVariant = computed(() => {
  const variants = {
    'en-route': 'info',
    'pickup': 'warning',
    'dropoff': 'success'
  }
  return variants[ride.value?.status] || 'default'
})

const statusText = computed(() => {
  const texts = {
    'en-route': 'En Route',
    'pickup': 'Pickup',
    'dropoff': 'Dropoff'
  }
  return texts[ride.value?.status] || ride.value?.status
})

onMounted(async () => {
  await loadRide()
})

const loadRide = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await rideStore.fetchRideById(rideId.value)
    ride.value = data
  } catch (err) {
    error.value = err || 'Failed to load ride details'
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  deleting.value = true
  try {
    await rideStore.deleteRide(rideId.value)
    router.push('/rides')
  } catch (err) {
    error.value = err || 'Failed to delete ride'
    showDeleteConfirm.value = false
  } finally {
    deleting.value = false
  }
}

const formatDateTime = (datetime) => {
  return dayjs(datetime).format('MMM D, YYYY h:mm A')
}

const formatRelativeTime = (datetime) => {
  return dayjs(datetime).fromNow()
}

const handleEdit = () => {
  showEditModal.value = true
}

const handleEditSubmit = async (payload) => {
  try {
    await rideStore.updateRide(rideId.value, payload)
    await loadRide() // Reload ride to get updated data
    showEditModal.value = false
  } catch (err) {
    error.value = err || 'Failed to update ride'
  }
}
</script>

<template>
  <MainLayout>
    <div class="max-w-5xl mx-auto">
      <!-- Back Button -->
      <button
        @click="router.push('/rides')"
        class="mb-4 text-sm text-gray-600 hover:text-gray-900 flex items-center gap-1"
      >
        ← Back to Rides
      </button>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>

      <!-- Error State -->
      <ErrorAlert
        v-else-if="error"
        :message="error"
        @dismiss="error = null"
        class="mb-6"
      />

      <!-- Ride Details -->
      <div v-else-if="ride" class="space-y-6">
        <!-- Header -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-start justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900 mb-2">
                Ride #{{ ride.id_ride }}
              </h1>
              <Badge :text="statusText" :variant="statusVariant" />
            </div>
            <div class="flex gap-2">
              <button
                @click="handleEdit"
                class="p-2 text-blue-600 hover:bg-blue-50 rounded-md"
                title="Edit Ride"
              >
                <PencilIcon class="w-5 h-5" />
              </button>
              <button
                @click="showDeleteConfirm = true"
                class="p-2 text-red-600 hover:bg-red-50 rounded-md"
                title="Delete Ride"
              >
                <TrashIcon class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        <!-- Rider & Driver Info -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Rider -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
              <UserIcon class="w-5 h-5" />
              Rider Information
            </h2>
            <div class="space-y-2">
              <div>
                <span class="text-sm text-gray-500">Name:</span>
                <p class="font-medium">{{ ride.rider.first_name }} {{ ride.rider.last_name }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">Email:</span>
                <p class="font-medium">{{ ride.rider.email }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">Phone:</span>
                <p class="font-medium">{{ ride.rider.phone_number }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">Role:</span>
                <p class="font-medium capitalize">{{ ride.rider.role }}</p>
              </div>
            </div>
          </div>

          <!-- Driver -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
              <UserIcon class="w-5 h-5" />
              Driver Information
            </h2>
            <div class="space-y-2">
              <div>
                <span class="text-sm text-gray-500">Name:</span>
                <p class="font-medium">{{ ride.driver.first_name }} {{ ride.driver.last_name }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">Email:</span>
                <p class="font-medium">{{ ride.driver.email }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">Phone:</span>
                <p class="font-medium">{{ ride.driver.phone_number }}</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">Role:</span>
                <p class="font-medium capitalize">{{ ride.driver.role }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Ride Details -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold mb-4">Ride Details</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div class="flex items-center gap-2 mb-2">
                <ClockIcon class="w-5 h-5 text-gray-400" />
                <span class="text-sm text-gray-500">Pickup Time:</span>
              </div>
              <p class="font-medium ml-7">{{ formatDateTime(ride.pickup_time) }}</p>
            </div>
            <div>
              <div class="flex items-center gap-2 mb-2">
                <MapPinIcon class="w-5 h-5 text-gray-400" />
                <span class="text-sm text-gray-500">Pickup Location:</span>
              </div>
              <p class="font-medium ml-7 text-sm">
                {{ ride.pickup_latitude.toFixed(6) }}, {{ ride.pickup_longitude.toFixed(6) }}
              </p>
            </div>
            <div>
              <div class="flex items-center gap-2 mb-2">
                <MapPinIcon class="w-5 h-5 text-gray-400" />
                <span class="text-sm text-gray-500">Dropoff Location:</span>
              </div>
              <p class="font-medium ml-7 text-sm">
                {{ ride.dropoff_latitude.toFixed(6) }}, {{ ride.dropoff_longitude.toFixed(6) }}
              </p>
            </div>
          </div>
        </div>

        <!-- Ride Events -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <ClipboardDocumentListIcon class="w-5 h-5" />
            Ride Events
            <span class="text-sm font-normal text-gray-500 ml-2">
              ({{ ride.ride_events?.length || 0 }} events)
            </span>
          </h2>

          <div v-if="ride.ride_events && ride.ride_events.length > 0" class="space-y-4">
            <!-- Timeline -->
            <div class="relative">
              <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>

              <div
                v-for="(event, index) in ride.ride_events"
                :key="event.id_ride_event"
                class="relative pl-10 pb-6 last:pb-0"
              >
                <!-- Timeline dot -->
                <div class="absolute left-2.5 w-3 h-3 bg-blue-500 rounded-full border-2 border-white"></div>

                <!-- Event content -->
                <div class="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors">
                  <div class="flex items-start justify-between gap-4">
                    <div class="flex-1">
                      <p class="font-medium text-gray-900">{{ event.description }}</p>
                      <p class="text-sm text-gray-500 mt-1">
                        {{ formatDateTime(event.created_at) }}
                      </p>
                    </div>
                    <span class="text-xs text-gray-400 whitespace-nowrap">
                      {{ formatRelativeTime(event.created_at) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-500">
            <ClipboardDocumentListIcon class="w-12 h-12 mx-auto mb-2 text-gray-300" />
            <p>No ride events recorded yet.</p>
          </div>
        </div>

      </div>

      <!-- Delete Confirmation Modal -->
      <div
        v-if="showDeleteConfirm"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="showDeleteConfirm = false"
      >
        <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
          <h3 class="text-lg font-semibold mb-2">Delete Ride?</h3>
          <p class="text-gray-600 mb-6">
            Are you sure you want to delete Ride #{{ ride?.id_ride }}? This action cannot be undone.
          </p>
          <div class="flex gap-3 justify-end">
            <button
              @click="showDeleteConfirm = false"
              :disabled="deleting"
              class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              @click="handleDelete"
              :disabled="deleting"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50 flex items-center gap-2"
            >
              <LoadingSpinner v-if="deleting" size="sm" />
              <span>{{ deleting ? 'Deleting...' : 'Delete' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Edit Modal -->
      <RideFormModal
        :show="showEditModal"
        :ride="ride"
        @close="showEditModal = false"
        @submit="handleEditSubmit"
      />
    </div>
  </MainLayout>
</template>
