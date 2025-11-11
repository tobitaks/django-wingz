import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import rideService from '../services/rideService'

export const useRideStore = defineStore('ride', () => {
  // State
  const rides = ref([])
  const currentRide = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Pagination
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalItems = ref(0)

  // Filters
  const filters = ref({
    status: '',
    rider_email: '',
    ordering: '-pickup_time', // Default: newest first
    latitude: null,
    longitude: null
  })

  // Getters
  const hasRides = computed(() => rides.value.length > 0)
  const isLoading = computed(() => loading.value)
  const hasError = computed(() => error.value !== null)

  // Actions
  async function fetchRides(params = {}) {
    loading.value = true
    error.value = null

    try {
      const queryParams = {
        page: currentPage.value,
        ...filters.value,
        ...params
      }

      // Remove empty filters
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === '' || queryParams[key] === null || queryParams[key] === undefined) {
          delete queryParams[key]
        }
      })

      const response = await rideService.getRides(queryParams)

      rides.value = response.data.results || []
      totalItems.value = response.data.count || 0

      // Calculate total pages (assuming PAGE_SIZE = 10 from backend)
      const pageSize = 10
      totalPages.value = Math.ceil(totalItems.value / pageSize)

      return response.data
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchRideById(id) {
    loading.value = true
    error.value = null

    try {
      const response = await rideService.getRideById(id)
      currentRide.value = response.data
      return response.data
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createRide(data) {
    loading.value = true
    error.value = null

    try {
      const response = await rideService.createRide(data)
      rides.value.unshift(response.data) // Add to beginning of list
      return response.data
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateRide(id, data) {
    loading.value = true
    error.value = null

    try {
      const response = await rideService.updateRide(id, data)
      const index = rides.value.findIndex(r => r.id_ride === id)
      if (index !== -1) {
        rides.value[index] = response.data
      }
      if (currentRide.value?.id_ride === id) {
        currentRide.value = response.data
      }
      return response.data
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteRide(id) {
    loading.value = true
    error.value = null

    try {
      await rideService.deleteRide(id)
      rides.value = rides.value.filter(r => r.id_ride !== id)
      if (currentRide.value?.id_ride === id) {
        currentRide.value = null
      }
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  function setPage(page) {
    currentPage.value = page
  }

  function setFilter(filterName, value) {
    filters.value[filterName] = value
    currentPage.value = 1 // Reset to first page when filter changes
  }

  function clearFilters() {
    filters.value = {
      status: '',
      rider_email: '',
      ordering: '-pickup_time',
      latitude: null,
      longitude: null
    }
    currentPage.value = 1
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    rides,
    currentRide,
    loading,
    error,
    currentPage,
    totalPages,
    totalItems,
    filters,

    // Getters
    hasRides,
    isLoading,
    hasError,

    // Actions
    fetchRides,
    fetchRideById,
    createRide,
    updateRide,
    deleteRide,
    setPage,
    setFilter,
    clearFilters,
    clearError
  }
})
