<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import ErrorAlert from '../common/ErrorAlert.vue'
import userService from '../../services/userService'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  ride: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'submit'])

const isEditMode = computed(() => !!props.ride)

// Form data
const formData = ref({
  status: 'en-route',
  rider: null,
  driver: null,
  pickup_latitude: '',
  pickup_longitude: '',
  dropoff_latitude: '',
  dropoff_longitude: '',
  pickup_time: ''
})

// Dropdown data
const riders = ref([])
const drivers = ref([])
const loadingUsers = ref(false)
const usersError = ref(null)

// Form state
const submitting = ref(false)
const error = ref(null)
const validationErrors = ref({})

// Status options
const statusOptions = [
  { value: 'en-route', label: 'En Route' },
  { value: 'pickup', label: 'Pickup' },
  { value: 'dropoff', label: 'Dropoff' }
]

// Functions
const resetForm = () => {
  formData.value = {
    status: 'en-route',
    rider: null,
    driver: null,
    pickup_latitude: '',
    pickup_longitude: '',
    dropoff_latitude: '',
    dropoff_longitude: '',
    pickup_time: ''
  }
  validationErrors.value = {}
  error.value = null
}

const loadUsers = async () => {
  loadingUsers.value = true
  usersError.value = null
  try {
    const response = await userService.getUsers()
    // API returns array directly (no pagination)
    const users = Array.isArray(response.data) ? response.data : response.data.results || response.data

    // Filter riders and drivers
    riders.value = users.filter(u => u.role === 'rider')
    drivers.value = users.filter(u => u.role === 'driver')
  } catch (err) {
    console.error('Load users error:', err)
    usersError.value = err?.message || 'Failed to load users'
  } finally {
    loadingUsers.value = false
  }
}

// Watch for ride prop changes to populate form in edit mode
watch(() => props.ride, (newRide) => {
  if (newRide) {
    formData.value = {
      status: newRide.status,
      rider: newRide.rider?.id_user || null,
      driver: newRide.driver?.id_user || null,
      pickup_latitude: newRide.pickup_latitude?.toString() || '',
      pickup_longitude: newRide.pickup_longitude?.toString() || '',
      dropoff_latitude: newRide.dropoff_latitude?.toString() || '',
      dropoff_longitude: newRide.dropoff_longitude?.toString() || '',
      pickup_time: newRide.pickup_time ? new Date(newRide.pickup_time).toISOString().slice(0, 16) : ''
    }
  } else {
    resetForm()
  }
}, { immediate: true })

// Load users on mount
onMounted(async () => {
  await loadUsers()
})

const validateForm = () => {
  const errors = {}

  if (!formData.value.rider) {
    errors.rider = 'Rider is required'
  }

  if (!formData.value.driver) {
    errors.driver = 'Driver is required'
  }

  if (!formData.value.pickup_latitude) {
    errors.pickup_latitude = 'Pickup latitude is required'
  } else if (isNaN(formData.value.pickup_latitude) || formData.value.pickup_latitude < -90 || formData.value.pickup_latitude > 90) {
    errors.pickup_latitude = 'Invalid latitude (-90 to 90)'
  }

  if (!formData.value.pickup_longitude) {
    errors.pickup_longitude = 'Pickup longitude is required'
  } else if (isNaN(formData.value.pickup_longitude) || formData.value.pickup_longitude < -180 || formData.value.pickup_longitude > 180) {
    errors.pickup_longitude = 'Invalid longitude (-180 to 180)'
  }

  if (!formData.value.dropoff_latitude) {
    errors.dropoff_latitude = 'Dropoff latitude is required'
  } else if (isNaN(formData.value.dropoff_latitude) || formData.value.dropoff_latitude < -90 || formData.value.dropoff_latitude > 90) {
    errors.dropoff_latitude = 'Invalid latitude (-90 to 90)'
  }

  if (!formData.value.dropoff_longitude) {
    errors.dropoff_longitude = 'Dropoff longitude is required'
  } else if (isNaN(formData.value.dropoff_longitude) || formData.value.dropoff_longitude < -180 || formData.value.dropoff_longitude > 180) {
    errors.dropoff_longitude = 'Invalid longitude (-180 to 180)'
  }

  if (!formData.value.pickup_time) {
    errors.pickup_time = 'Pickup time is required'
  }

  validationErrors.value = errors
  return Object.keys(errors).length === 0
}

const handleSubmit = async () => {
  error.value = null

  if (!validateForm()) {
    return
  }

  submitting.value = true

  try {
    const payload = {
      status: formData.value.status,
      id_rider_id: formData.value.rider,
      id_driver_id: formData.value.driver,
      pickup_latitude: parseFloat(formData.value.pickup_latitude),
      pickup_longitude: parseFloat(formData.value.pickup_longitude),
      dropoff_latitude: parseFloat(formData.value.dropoff_latitude),
      dropoff_longitude: parseFloat(formData.value.dropoff_longitude),
      pickup_time: new Date(formData.value.pickup_time).toISOString()
    }

    emit('submit', payload)
  } catch (err) {
    error.value = err || 'Failed to save ride'
  } finally {
    submitting.value = false
  }
}

const handleClose = () => {
  if (!submitting.value) {
    resetForm()
    emit('close')
  }
}
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    @click.self="handleClose"
  >
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b">
        <h2 class="text-xl font-semibold">
          {{ isEditMode ? 'Edit Ride' : 'Create New Ride' }}
        </h2>
        <button
          @click="handleClose"
          :disabled="submitting"
          class="text-gray-400 hover:text-gray-600 disabled:opacity-50"
        >
          <XMarkIcon class="w-6 h-6" />
        </button>
      </div>

      <!-- Body -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        <!-- Error Alert -->
        <ErrorAlert
          v-if="error"
          :message="error"
          @dismiss="error = null"
        />

        <!-- Users Loading Error -->
        <ErrorAlert
          v-if="usersError"
          :message="usersError"
          @dismiss="usersError = null"
        />

        <!-- Status -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Status <span class="text-red-500">*</span>
          </label>
          <select
            v-model="formData.status"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="submitting"
          >
            <option v-for="option in statusOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>

        <!-- Rider -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Rider <span class="text-red-500">*</span>
          </label>
          <select
            v-model="formData.rider"
            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="validationErrors.rider ? 'border-red-500' : 'border-gray-300'"
            :disabled="submitting || loadingUsers"
          >
            <option :value="null">Select a rider</option>
            <option v-for="rider in riders" :key="rider.id_user" :value="rider.id_user">
              {{ rider.first_name }} {{ rider.last_name }} ({{ rider.email }})
            </option>
          </select>
          <p v-if="validationErrors.rider" class="text-red-500 text-sm mt-1">
            {{ validationErrors.rider }}
          </p>
        </div>

        <!-- Driver -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Driver <span class="text-red-500">*</span>
          </label>
          <select
            v-model="formData.driver"
            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="validationErrors.driver ? 'border-red-500' : 'border-gray-300'"
            :disabled="submitting || loadingUsers"
          >
            <option :value="null">Select a driver</option>
            <option v-for="driver in drivers" :key="driver.id_user" :value="driver.id_user">
              {{ driver.first_name }} {{ driver.last_name }} ({{ driver.email }})
            </option>
          </select>
          <p v-if="validationErrors.driver" class="text-red-500 text-sm mt-1">
            {{ validationErrors.driver }}
          </p>
        </div>

        <!-- Pickup Location -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Pickup Latitude <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.pickup_latitude"
              type="number"
              step="any"
              placeholder="-90 to 90"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="validationErrors.pickup_latitude ? 'border-red-500' : 'border-gray-300'"
              :disabled="submitting"
            />
            <p v-if="validationErrors.pickup_latitude" class="text-red-500 text-sm mt-1">
              {{ validationErrors.pickup_latitude }}
            </p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Pickup Longitude <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.pickup_longitude"
              type="number"
              step="any"
              placeholder="-180 to 180"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="validationErrors.pickup_longitude ? 'border-red-500' : 'border-gray-300'"
              :disabled="submitting"
            />
            <p v-if="validationErrors.pickup_longitude" class="text-red-500 text-sm mt-1">
              {{ validationErrors.pickup_longitude }}
            </p>
          </div>
        </div>

        <!-- Dropoff Location -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Dropoff Latitude <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.dropoff_latitude"
              type="number"
              step="any"
              placeholder="-90 to 90"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="validationErrors.dropoff_latitude ? 'border-red-500' : 'border-gray-300'"
              :disabled="submitting"
            />
            <p v-if="validationErrors.dropoff_latitude" class="text-red-500 text-sm mt-1">
              {{ validationErrors.dropoff_latitude }}
            </p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Dropoff Longitude <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.dropoff_longitude"
              type="number"
              step="any"
              placeholder="-180 to 180"
              class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="validationErrors.dropoff_longitude ? 'border-red-500' : 'border-gray-300'"
              :disabled="submitting"
            />
            <p v-if="validationErrors.dropoff_longitude" class="text-red-500 text-sm mt-1">
              {{ validationErrors.dropoff_longitude }}
            </p>
          </div>
        </div>

        <!-- Pickup Time -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Pickup Time <span class="text-red-500">*</span>
          </label>
          <input
            v-model="formData.pickup_time"
            type="datetime-local"
            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :class="validationErrors.pickup_time ? 'border-red-500' : 'border-gray-300'"
            :disabled="submitting"
          />
          <p v-if="validationErrors.pickup_time" class="text-red-500 text-sm mt-1">
            {{ validationErrors.pickup_time }}
          </p>
        </div>

        <!-- Footer -->
        <div class="flex gap-3 justify-end pt-4 border-t">
          <button
            type="button"
            @click="handleClose"
            :disabled="submitting"
            class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="submitting || loadingUsers"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <LoadingSpinner v-if="submitting" size="sm" />
            <span>{{ submitting ? 'Saving...' : (isEditMode ? 'Update Ride' : 'Create Ride') }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
