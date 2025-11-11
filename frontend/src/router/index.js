import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import RideListView from '../views/RideListView.vue'
import RideDetailView from '../views/RideDetailView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: '/rides'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/rides',
    name: 'rides',
    component: RideListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/rides/:id',
    name: 'ride-detail',
    component: RideDetailView,
    meta: { requiresAuth: true }
  },
  // More routes will be added in subsequent phases
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard for authentication
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Check if route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

  if (requiresAuth) {
    // Check authentication status if not already checked
    if (!authStore.isAuthenticated && !authStore.user) {
      try {
        await authStore.checkAuth()
      } catch (error) {
        // Failed to check auth, continue anyway
      }
    }

    if (!authStore.isAuthenticated) {
      // Not authenticated, redirect to login
      next({ name: 'login' })
    } else {
      // Authenticated, proceed
      next()
    }
  } else {
    // Route doesn't require auth
    if (to.name === 'login' && authStore.isAuthenticated) {
      // Already logged in, redirect to rides
      next({ name: 'rides' })
    } else {
      next()
    }
  }
})

export default router
