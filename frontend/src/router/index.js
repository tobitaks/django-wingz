import { createRouter, createWebHistory } from 'vue-router'
import RideListView from '../views/RideListView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: '/rides'
  },
  {
    path: '/rides',
    name: 'rides',
    component: RideListView
  },
  // More routes will be added in subsequent phases
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
