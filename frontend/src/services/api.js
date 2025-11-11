import axios from 'axios'

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  withCredentials: true, // Important for Django session authentication
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add CSRF token for non-GET requests
    if (config.method !== 'get') {
      const csrfToken = getCookie('csrftoken')
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response

      if (status === 401) {
        // Unauthorized - redirect to login
        console.error('Unauthorized access')
      } else if (status === 403) {
        // Forbidden
        console.error('Forbidden access')
      } else if (status === 404) {
        // Not found
        console.error('Resource not found')
      } else if (status >= 500) {
        // Server error
        console.error('Server error')
      }

      // Return error message from server or generic message
      return Promise.reject(data?.detail || data || 'An error occurred')
    } else if (error.request) {
      // Request made but no response received
      return Promise.reject('Network error - please check your connection')
    } else {
      // Error in request setup
      return Promise.reject(error.message)
    }
  }
)

export default api
