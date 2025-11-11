<script setup>
import MainLayout from '../components/layout/MainLayout.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ErrorAlert from '../components/common/ErrorAlert.vue'
import EmptyState from '../components/common/EmptyState.vue'
import Badge from '../components/common/Badge.vue'
import Pagination from '../components/common/Pagination.vue'

// Demo state for testing components
import { ref } from 'vue'
const showError = ref(false)
const currentPage = ref(1)
</script>

<template>
  <MainLayout>
    <div class="max-w-7xl mx-auto">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">
        Rides
      </h1>

      <!-- Demo Components -->
      <div class="space-y-6">
        <!-- Success message -->
        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
          <p class="text-sm text-green-800">
            ✅ Phase 2 Complete! Layout and common components working.
          </p>
        </div>

        <!-- Component Demo -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold mb-4">Component Preview</h2>

          <div class="space-y-4">
            <!-- Badges -->
            <div class="flex gap-2 flex-wrap">
              <Badge text="En-route" variant="info" />
              <Badge text="Pickup" variant="warning" />
              <Badge text="Dropoff" variant="success" />
              <Badge text="Error" variant="error" />
            </div>

            <!-- Loading Spinner -->
            <div class="flex gap-4 items-center">
              <LoadingSpinner size="sm" />
              <LoadingSpinner size="md" />
              <LoadingSpinner size="lg" />
            </div>

            <!-- Error Alert Toggle -->
            <div>
              <button
                @click="showError = !showError"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Toggle Error Alert
              </button>
              <ErrorAlert
                v-if="showError"
                message="This is a test error message. You can dismiss it."
                @dismiss="showError = false"
                class="mt-2"
              />
            </div>

            <!-- Empty State -->
            <EmptyState
              title="No rides found"
              message="Get started by creating your first ride."
            />

            <!-- Pagination -->
            <Pagination
              :current-page="currentPage"
              :total-pages="10"
              :total-items="100"
              @page-change="(page) => currentPage = page"
            />
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<style scoped>
/* Component styles will go here */
</style>
