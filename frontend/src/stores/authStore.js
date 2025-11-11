import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '../services/authService'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const currentUser = computed(() => user.value)
  const isAdmin = computed(() => user.value?.is_staff || user.value?.is_superuser)
  const isLoading = computed(() => loading.value)

  // Actions
  async function login(credentials) {
    loading.value = true
    error.value = null

    try {
      const response = await authService.login(credentials)
      user.value = response.data.user
      isAuthenticated.value = true
      return response.data
    } catch (err) {
      error.value = err
      isAuthenticated.value = false
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    error.value = null

    try {
      await authService.logout()
      user.value = null
      isAuthenticated.value = false
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  async function checkAuth() {
    loading.value = true
    error.value = null

    try {
      const response = await authService.checkAuth()
      user.value = response.data.user
      isAuthenticated.value = response.data.authenticated
      return response.data
    } catch (err) {
      user.value = null
      isAuthenticated.value = false
      error.value = err
    } finally {
      loading.value = false
    }
  }

  async function getCurrentUser() {
    loading.value = true
    error.value = null

    try {
      const response = await authService.getCurrentUser()
      user.value = response.data
      isAuthenticated.value = true
      return response.data
    } catch (err) {
      user.value = null
      isAuthenticated.value = false
      error.value = err
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    user,
    isAuthenticated,
    loading,
    error,

    // Getters
    currentUser,
    isAdmin,
    isLoading,

    // Actions
    login,
    logout,
    checkAuth,
    getCurrentUser,
    clearError
  }
})
