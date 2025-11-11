import api from './api'

const authService = {
  /**
   * Get CSRF token
   * @returns {Promise} Response
   */
  getCsrfToken() {
    return api.get('/auth/csrf/')
  },

  /**
   * Login user with credentials
   * @param {Object} credentials - Login credentials
   * @param {string} credentials.username - Username
   * @param {string} credentials.password - Password
   * @returns {Promise} Response with user data and token
   */
  async login(credentials) {
    // Get CSRF token first
    await this.getCsrfToken()
    // Then login
    return api.post('/auth/login/', credentials)
  },

  /**
   * Logout current user
   * @returns {Promise} Response
   */
  logout() {
    return api.post('/auth/logout/')
  },

  /**
   * Get current authenticated user
   * @returns {Promise} Response with user data
   */
  getCurrentUser() {
    return api.get('/auth/user/')
  },

  /**
   * Check if user is authenticated
   * @returns {Promise} Response with auth status
   */
  checkAuth() {
    return api.get('/auth/check/')
  }
}

export default authService
