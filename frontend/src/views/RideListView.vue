<script setup>
import { ref, onMounted } from 'vue'
import { useRideStore } from '../stores/rideStore'
import MainLayout from '../components/layout/MainLayout.vue'
import RideCard from '../components/rides/RideCard.vue'
import RideFilters from '../components/rides/RideFilters.vue'
import RideFormModal from '../components/rides/RideFormModal.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ErrorAlert from '../components/common/ErrorAlert.vue'
import EmptyState from '../components/common/EmptyState.vue'
import Pagination from '../components/common/Pagination.vue'
import { PlusIcon } from '@heroicons/vue/24/outline'

const rideStore = useRideStore()
const showCreateModal = ref(false)

onMounted(async () => {
  await loadRides()
})

const loadRides = async () => {
  try {
    await rideStore.fetchRides()
  } catch (error) {
    console.error('Failed to fetch rides:', error)
  }
}

const handleFilterChange = () => {
  rideStore.setPage(1) // Reset to first page on filter change
  loadRides()
}

const handlePageChange = (page) => {
  rideStore.setPage(page)
  loadRides()
  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleCreateSubmit = async (payload) => {
  try {
    await rideStore.createRide(payload)
    await loadRides() // Reload rides list
    showCreateModal.value = false
  } catch (err) {
    // Error is already set in the store, modal will display it
    console.error('Failed to create ride:', err)
  }
}
</script>

<template>
  <MainLayout>
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-6 flex items-start justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Rides</h1>
          <p class="text-sm text-gray-600 mt-1">
            Manage and view all ride information
          </p>
        </div>
        <button
          @click="showCreateModal = true"
          class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          <PlusIcon class="w-5 h-5" />
          <span>Create Ride</span>
        </button>
      </div>

      <!-- Filters -->
      <div class="mb-6">
        <RideFilters
          v-model="rideStore.filters"
          @apply="handleFilterChange"
        />
      </div>

      <!-- Error Alert -->
      <ErrorAlert
        v-if="rideStore.hasError"
        :message="rideStore.error"
        @dismiss="rideStore.clearError"
        class="mb-6"
      />

      <!-- Loading State -->
      <div v-if="rideStore.isLoading && !rideStore.hasRides" class="flex justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>

      <!-- Rides Grid -->
      <div v-else-if="rideStore.hasRides" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <RideCard
            v-for="ride in rideStore.rides"
            :key="ride.id_ride"
            :ride="ride"
          />
        </div>

        <!-- Pagination -->
        <Pagination
          v-if="rideStore.totalPages > 1"
          :current-page="rideStore.currentPage"
          :total-pages="rideStore.totalPages"
          :total-items="rideStore.totalItems"
          @page-change="handlePageChange"
        />
      </div>

      <!-- Empty State -->
      <EmptyState
        v-else
        title="No rides found"
        message="No rides match your current filters. Try adjusting your search criteria."
      />

      <!-- Loading Overlay (for pagination/filter changes) -->
      <div
        v-if="rideStore.isLoading && rideStore.hasRides"
        class="fixed inset-0 bg-black bg-opacity-10 flex items-center justify-center z-50"
      >
        <div class="bg-white rounded-lg p-6 shadow-lg">
          <LoadingSpinner size="lg" />
          <p class="text-sm text-gray-600 mt-3">Loading rides...</p>
        </div>
      </div>

      <!-- Create Modal -->
      <RideFormModal
        :show="showCreateModal"
        @close="showCreateModal = false"
        @submit="handleCreateSubmit"
      />
    </div>
  </MainLayout>
</template>
