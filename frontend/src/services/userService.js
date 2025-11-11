import api from './api'

const userService = {
  /**
   * Get all users
   * @param {Object} params - Query parameters
   * @returns {Promise} Response with users data
   */
  getUsers(params = {}) {
    return api.get('/users/', { params })
  },

  /**
   * Get a single user by ID
   * @param {number} id - User ID
   * @returns {Promise} Response with user data
   */
  getUserById(id) {
    return api.get(`/users/${id}/`)
  },

  /**
   * Create a new user
   * @param {Object} data - User data
   * @returns {Promise} Response with created user data
   */
  createUser(data) {
    return api.post('/users/', data)
  },

  /**
   * Update an existing user
   * @param {number} id - User ID
   * @param {Object} data - Updated user data
   * @returns {Promise} Response with updated user data
   */
  updateUser(id, data) {
    return api.put(`/users/${id}/`, data)
  },

  /**
   * Delete a user
   * @param {number} id - User ID
   * @returns {Promise} Response
   */
  deleteUser(id) {
    return api.delete(`/users/${id}/`)
  }
}

export default userService
