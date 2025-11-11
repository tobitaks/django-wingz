<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { LockClosedIcon, UserIcon } from '@heroicons/vue/24/outline'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ErrorAlert from '../components/common/ErrorAlert.vue'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password'
    return
  }

  loading.value = true
  error.value = null

  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })

    // Redirect to rides page after successful login
    router.push('/rides')
  } catch (err) {
    error.value = err || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo/Header -->
      <div class="text-center">
        <h2 class="text-3xl font-bold text-gray-900">
          Wingz Ride Management
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Sign in to your account
        </p>
      </div>

      <!-- Login Form -->
      <div class="bg-white rounded-lg shadow-md p-8">
        <!-- Error Alert -->
        <ErrorAlert
          v-if="error"
          :message="error"
          @dismiss="error = null"
          class="mb-6"
        />

        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <div class="relative">
              <input
                id="username"
                v-model="username"
                type="text"
                required
                autocomplete="username"
                :disabled="loading"
                class="w-full px-3 py-2 pl-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                placeholder="Enter your username"
              />
              <UserIcon class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                type="password"
                required
                autocomplete="current-password"
                :disabled="loading"
                class="w-full px-3 py-2 pl-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                placeholder="Enter your password"
              />
              <LockClosedIcon class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center items-center gap-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <LoadingSpinner v-if="loading" size="sm" />
            <span>{{ loading ? 'Signing in...' : 'Sign in' }}</span>
          </button>
        </form>

        <!-- Help Text -->
        <div class="mt-6 text-center">
          <p class="text-xs text-gray-500">
            Use your admin credentials to access the dashboard
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
