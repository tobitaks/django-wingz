import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUiStore = defineStore('ui', () => {
  // State
  const sidebarOpen = ref(false)
  const toast = ref({
    show: false,
    message: '',
    type: 'info' // info, success, warning, error
  })

  // Getters
  const isSidebarOpen = computed(() => sidebarOpen.value)
  const hasToast = computed(() => toast.value.show)

  // Actions
  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  function openSidebar() {
    sidebarOpen.value = true
  }

  function closeSidebar() {
    sidebarOpen.value = false
  }

  function showToast(message, type = 'info', duration = 3000) {
    toast.value = {
      show: true,
      message,
      type
    }

    if (duration > 0) {
      setTimeout(() => {
        hideToast()
      }, duration)
    }
  }

  function hideToast() {
    toast.value.show = false
  }

  function showSuccess(message, duration = 3000) {
    showToast(message, 'success', duration)
  }

  function showError(message, duration = 5000) {
    showToast(message, 'error', duration)
  }

  function showWarning(message, duration = 4000) {
    showToast(message, 'warning', duration)
  }

  function showInfo(message, duration = 3000) {
    showToast(message, 'info', duration)
  }

  return {
    // State
    sidebarOpen,
    toast,

    // Getters
    isSidebarOpen,
    hasToast,

    // Actions
    toggleSidebar,
    openSidebar,
    closeSidebar,
    showToast,
    hideToast,
    showSuccess,
    showError,
    showWarning,
    showInfo
  }
})
