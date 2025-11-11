<script setup>
import { HomeIcon, MapIcon, UserGroupIcon } from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router'

defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close'])
const router = useRouter()

const navigation = [
  { name: 'Rides', to: '/rides', icon: HomeIcon },
  { name: 'Map View', to: '/map', icon: MapIcon },
  { name: 'Users', to: '/users', icon: UserGroupIcon },
]

const navigateTo = (to) => {
  router.push(to)
  emit('close')
}
</script>

<template>
  <!-- Mobile Overlay -->
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
    @click="emit('close')"
  ></div>

  <!-- Sidebar -->
  <aside
    :class="[
      'fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 transition-transform duration-300',
      isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
    ]"
  >
    <nav class="p-4 space-y-2">
      <button
        v-for="item in navigation"
        :key="item.name"
        @click="navigateTo(item.to)"
        class="w-full flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <component :is="item.icon" class="w-5 h-5" />
        <span class="font-medium">{{ item.name }}</span>
      </button>
    </nav>
  </aside>
</template>

<style scoped>
/* Sidebar styles */
</style>
