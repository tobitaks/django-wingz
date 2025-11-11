import api from './api'

const rideService = {
  /**
   * Get all rides with optional filters, sorting, and pagination
   * @param {Object} params - Query parameters
   * @param {number} params.page - Page number
   * @param {string} params.status - Filter by status (en-route, pickup, dropoff)
   * @param {string} params.rider_email - Filter by rider email
   * @param {string} params.ordering - Sort by field (pickup_time, -pickup_time)
   * @param {number} params.latitude - GPS latitude for distance sorting
   * @param {number} params.longitude - GPS longitude for distance sorting
   * @returns {Promise} Response with rides data
   */
  getRides(params = {}) {
    return api.get('/rides/', { params })
  },

  /**
   * Get a single ride by ID
   * @param {number} id - Ride ID
   * @returns {Promise} Response with ride data
   */
  getRideById(id) {
    return api.get(`/rides/${id}/`)
  },

  /**
   * Create a new ride
   * @param {Object} data - Ride data
   * @returns {Promise} Response with created ride data
   */
  createRide(data) {
    return api.post('/rides/', data)
  },

  /**
   * Update an existing ride
   * @param {number} id - Ride ID
   * @param {Object} data - Updated ride data
   * @returns {Promise} Response with updated ride data
   */
  updateRide(id, data) {
    return api.put(`/rides/${id}/`, data)
  },

  /**
   * Partially update a ride
   * @param {number} id - Ride ID
   * @param {Object} data - Partial ride data
   * @returns {Promise} Response with updated ride data
   */
  patchRide(id, data) {
    return api.patch(`/rides/${id}/`, data)
  },

  /**
   * Delete a ride
   * @param {number} id - Ride ID
   * @returns {Promise} Response
   */
  deleteRide(id) {
    return api.delete(`/rides/${id}/`)
  }
}

export default rideService
