<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
import { Bars3Icon, ArrowRightOnRectangleIcon } from '@heroicons/vue/24/outline'

defineProps({
  sidebarOpen: Boolean
})

const emit = defineEmits(['toggle-sidebar'])
const router = useRouter()
const authStore = useAuthStore()

const userInitial = computed(() => {
  const user = authStore.currentUser
  if (user?.first_name) {
    return user.first_name.charAt(0).toUpperCase()
  }
  return 'A'
})

const userName = computed(() => {
  const user = authStore.currentUser
  if (user?.first_name && user?.last_name) {
    return `${user.first_name} ${user.last_name}`
  }
  return 'Admin User'
})

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>

<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="px-4 py-4 flex items-center justify-between">
      <!-- Logo and Menu Toggle -->
      <div class="flex items-center gap-4">
        <button
          @click="emit('toggle-sidebar')"
          class="lg:hidden p-2 rounded-md hover:bg-gray-100"
        >
          <Bars3Icon class="w-6 h-6 text-gray-600" />
        </button>
        <h1 class="text-xl font-bold text-gray-900">
          Wingz Ride Management
        </h1>
      </div>

      <!-- User Info -->
      <div class="flex items-center gap-3">
        <span class="text-sm text-gray-600 hidden sm:inline">{{ userName }}</span>
        <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
          <span class="text-white text-sm font-medium">{{ userInitial }}</span>
        </div>
        <button
          @click="handleLogout"
          class="p-2 rounded-md hover:bg-gray-100 text-gray-600 hover:text-gray-900"
          title="Logout"
        >
          <ArrowRightOnRectangleIcon class="w-5 h-5" />
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* Header styles */
</style>
