<script setup>
import { onMounted } from 'vue'
import { useRideStore } from '../stores/rideStore'
import MainLayout from '../components/layout/MainLayout.vue'
import RideCard from '../components/rides/RideCard.vue'
import RideFilters from '../components/rides/RideFilters.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ErrorAlert from '../components/common/ErrorAlert.vue'
import EmptyState from '../components/common/EmptyState.vue'
import Pagination from '../components/common/Pagination.vue'

const rideStore = useRideStore()

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
</script>

<template>
  <MainLayout>
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Rides</h1>
        <p class="text-sm text-gray-600 mt-1">
          Manage and view all ride information
        </p>
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
    </div>
  </MainLayout>
</template>
